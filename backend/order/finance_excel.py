"""
finance_excel.py
================
Ekspor laporan keuangan Masashimura ke Excel — dibangun sepenuhnya dari kode.

FITUR UTAMA:
  - Logo asli di-embed di Cover (PNG dari LOGO_PATH, fallback ke teks)
  - Tanggal generate OTOMATIS dari timezone.now() — tidak perlu di-hardcode
  - Mendukung mode BULANAN (rekap per hari) dan TAHUNAN (rekap per bulan)
  - Semua sheet: Cover, Control Panel, Rekap Periode, Ringkasan,
                 Detail Transaksi, Top Menu, Pengeluaran

Dipanggil dari view Django melalui export_finance_excel_view().
"""

import calendar
import io
import os

from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import ExtractMonth, TruncDate
from django.http import HttpResponse
from django.utils import timezone

from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from finance.models import Expense
from .models import Order, OrderItem

# ── Path ke logo ─────────────────────────────────────────────────────────────
# Letakkan file PNG logo di sini, atau atur via settings.EXCEL_LOGO_PATH
try:
    from django.conf import settings
    LOGO_PATH = getattr(
        settings,
        "EXCEL_LOGO_PATH",
        os.path.join(settings.BASE_DIR, "assets", "masashimura-logo.png"),
    )
except Exception:
    LOGO_PATH = "assets/masashimura-logo.png"

# ── Nama bulan Bahasa Indonesia ───────────────────────────────────────────────
BULAN_ID = {
    1: "Januari",   2: "Februari",  3: "Maret",     4: "April",
    5: "Mei",       6: "Juni",      7: "Juli",       8: "Agustus",
    9: "September", 10: "Oktober",  11: "November",  12: "Desember",
}

# ── Number formats ────────────────────────────────────────────────────────────
FMT_RP    = "#,##0"
FMT_PCT   = "0.00%"
FMT_DATE  = "DD/MM/YYYY"
FMT_INT   = "#,##0"

# ── Color palette ─────────────────────────────────────────────────────────────
C_DARK      = "111827"
C_DARK2     = "1F2937"
C_DARK3     = "374151"
C_GRAY      = "6B7280"
C_LIGHT     = "F9FAFB"
C_STRIPE    = "F3F4F6"
C_WHITE     = "FFFFFF"
C_RED       = "CC0000"
C_GOLD      = "F59E0B"
C_GREEN     = "059669"
C_BLUE      = "2563EB"
C_ORANGE    = "D97706"
C_PURPLE    = "7C3AED"
C_RED_LT    = "FEE2E2"
C_GRN_LT    = "D1FAE5"
C_YLW_LT    = "FEF3C7"
C_BLUE_LT   = "EFF6FF"

# ── Sheet names & tab colors ──────────────────────────────────────────────────
SH_COVER    = "🏠 Cover"
SH_CTRL     = "⚙ Control Panel"
SH_REKAP    = "📊 Rekap Periode"
SH_RING     = "📋 Ringkasan"
SH_DETAIL   = "📄 Detail Transaksi"
SH_TOPMENU  = "🍜 Top Menu"
SH_EXPENSE  = "💰 Pengeluaran"

TAB_COLORS = {
    SH_COVER:   C_DARK,
    SH_CTRL:    C_GRAY,
    SH_REKAP:   C_BLUE,
    SH_RING:    C_GREEN,
    SH_DETAIL:  C_ORANGE,
    SH_TOPMENU: "DC2626",
    SH_EXPENSE: C_PURPLE,
}


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def _fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


def _font(bold=False, size=10, color=C_DARK, italic=False, name="Arial") -> Font:
    return Font(bold=bold, size=size, color=color, italic=italic, name=name)


def _align(h="left", v="center", wrap=False) -> Alignment:
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)


def _border_thin(color="E5E7EB") -> Border:
    s = Side(style="thin", color=color)
    return Border(left=s, right=s, top=s, bottom=s)


def _border_bottom(color="E5E7EB") -> Border:
    return Border(bottom=Side(style="thin", color=color))


def _set_col_widths(ws, widths: dict):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


def _set_row_height(ws, row: int, height: float):
    ws.row_dimensions[row].height = height


def _write(ws, row, col, val, bold=False, size=10, color=C_DARK,
           bg=None, italic=False, h="left", v="center", wrap=False,
           num_fmt=None, border=None):
    """Tulis satu sel dengan style lengkap."""
    c = ws.cell(row, col, val)
    c.font = _font(bold, size, color, italic)
    if bg:
        c.fill = _fill(bg)
    c.alignment = _align(h, v, wrap)
    if num_fmt:
        c.number_format = num_fmt
    if border:
        c.border = border
    return c


def _merge(ws, r1, c1, r2, c2, val="", bold=False, size=10,
           color=C_DARK, bg=None, italic=False, h="left", v="center"):
    """Merge sel dan tulis nilai."""
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    c = ws.cell(r1, c1, val)
    c.font = _font(bold, size, color, italic)
    if bg:
        c.fill = _fill(bg)
    c.alignment = _align(h, v)
    return c


def _banner(ws, row, col_start, col_end, text, bg, height=50, size=16):
    """Banner penuh satu baris."""
    _set_row_height(ws, row, height)
    _merge(ws, row, col_start, row, col_end, text,
           bold=True, size=size, color=C_WHITE, bg=bg, h="left", v="center")


def _section_header(ws, row, col_start, col_end, text, height=28):
    """Sub-header abu gelap."""
    _set_row_height(ws, row, height)
    _merge(ws, row, col_start, row, col_end, "  " + text,
           bold=True, size=11, color=C_WHITE, bg=C_DARK3, h="left", v="center")


def _table_header(ws, row, headers, start_col=1, bg=C_DARK, fg=C_WHITE, height=24):
    """Baris header tabel."""
    _set_row_height(ws, row, height)
    for i, h in enumerate(headers):
        c = ws.cell(row, start_col + i, h)
        c.font = Font(bold=True, color=fg, name="Arial", size=10)
        c.fill = _fill(bg)
        c.alignment = _align("center")
        c.border = Border(bottom=Side(style="medium", color=bg))
    ws.freeze_panes = ws.cell(row + 1, 1).coordinate


def _auto_width(ws, min_w=8, max_w=42, extra=3):
    for col in ws.columns:
        mx = 0
        letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                v = str(cell.value or "")
                if len(v) > mx:
                    mx = len(v)
            except Exception:
                pass
        ws.column_dimensions[letter].width = min(max(mx + extra, min_w), max_w)


def _map_status(s: str) -> str:
    return {"paid": "Lunas", "pending": "Pending", "unpaid": "Pending"}.get(s, s.capitalize())


def _map_source(s: str) -> str:
    return "Web" if s == "web" else "POS"


# ═══════════════════════════════════════════════════════════════════════════════
# TANGGAL GENERATE — otomatis dari Django timezone
# ═══════════════════════════════════════════════════════════════════════════════

def _now_label() -> str:
    """
    Kembalikan tanggal & waktu generate dalam format:
    'Jumat, 26 Juni 2026 — 14:35 WIB'
    Dipanggil SAAT generate, bukan di-hardcode.
    """
    HARI_ID = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat",
        "Saturday": "Sabtu", "Sunday": "Minggu",
    }
    now = timezone.localtime(timezone.now())
    hari = HARI_ID.get(now.strftime("%A"), now.strftime("%A"))
    return (
        f"{hari}, {now.day} {BULAN_ID[now.month]} {now.year}"
        f" — {now.strftime('%H:%M')} WIB"
    )


def _short_date(dt) -> str:
    """'26 Juni 2026'"""
    return f"{dt.day} {BULAN_ID[dt.month]} {dt.year}"


def _build_filename(mode: str, month: int | None, year: int) -> str:
    if mode == "monthly" and month:
        return f"Rekap Finance Masashimura {BULAN_ID[month]} {year}.xlsx"
    return f"Rekap Finance Masashimura Tahun {year}.xlsx"


# ═══════════════════════════════════════════════════════════════════════════════
# WORKBOOK FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def _create_workbook() -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)
    for name in [SH_COVER, SH_CTRL, SH_REKAP, SH_RING, SH_DETAIL, SH_TOPMENU, SH_EXPENSE]:
        ws = wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        ws.sheet_properties.tabColor = TAB_COLORS[name]
    return wb


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1: 🏠 COVER
# ═══════════════════════════════════════════════════════════════════════════════

def _write_cover(wb, period_label: str, generated_at: str,
                 mode: str, year: int,
                 total_pendapatan: float, total_pengeluaran: float,
                 total_laba: float):
    ws = wb[SH_COVER]

    # Kolom: A=spacer, B=margin, C..F=konten(4 col), G=margin, H=spacer
    _set_col_widths(ws, {"A": 1.5, "B": 2, "C": 22, "D": 22, "E": 22, "F": 22, "G": 2, "H": 1.5})

    # Background gelap full
    for r in range(1, 40):
        _set_row_height(ws, r, 18)
        for col in "ABCDEFGH":
            ws[f"{col}{r}"].fill = _fill(C_DARK)

    # ── Red accent bar (rows 1-2) ────────────────────────────────────────────
    for r in (1, 2):
        _set_row_height(ws, r, 6)
        for col in "BCDEFG":
            ws[f"{col}{r}"].fill = _fill(C_RED)

    # ── LOGO (row 4-9) ───────────────────────────────────────────────────────
    logo_written = False
    if os.path.isfile(LOGO_PATH):
        try:
            from PIL import Image as PILImage

            pil_img = PILImage.open(LOGO_PATH).convert("RGBA")
            orig_w, orig_h = pil_img.size

            # Target lebar 480px, jaga aspect ratio
            target_w = 480
            target_h = max(1, int(orig_h * target_w / orig_w))
            pil_img  = pil_img.resize((target_w, target_h), PILImage.LANCZOS)

            buf = io.BytesIO()
            # Flatten ke PNG dengan background gelap agar transparan terlihat bagus
            bg = PILImage.new("RGBA", pil_img.size, (17, 24, 39, 255))  # #111827
            merged = PILImage.alpha_composite(bg, pil_img).convert("RGB")
            merged.save(buf, format="PNG")
            buf.seek(0)

            xl_img = XLImage(buf)
            xl_img.anchor = "C4"
            # Atur ukuran agar muat dalam ~5 baris
            xl_img.width  = target_w
            xl_img.height = target_h
            ws.add_image(xl_img)

            # Tinggi baris 4-9 disesuaikan tinggi gambar (px → pt ~0.75)
            logo_rows = 6
            row_h = max(18, int(target_h / logo_rows * 0.85))
            for r in range(4, 4 + logo_rows):
                _set_row_height(ws, r, row_h)
                for col in "CDEFG":
                    ws[f"{col}{r}"].fill = _fill(C_DARK)

            logo_written = True
        except Exception:
            pass  # fallback ke teks di bawah

    if not logo_written:
        _set_row_height(ws, 4, 8)
        _set_row_height(ws, 5, 60)
        _set_row_height(ws, 6, 8)
        ws.merge_cells("C5:F5")
        fb = ws["C5"]
        fb.value = "MASASHIMURA"
        fb.font  = Font(bold=True, size=36, color=C_GOLD, name="Arial Black")
        fb.fill  = _fill(C_DARK)
        fb.alignment = _align("center", "center")

    # ── Gold underline ────────────────────────────────────────────────────────
    AFTER_LOGO = 10
    _set_row_height(ws, AFTER_LOGO, 4)
    for col in "CDEF":
        ws[f"{col}{AFTER_LOGO}"].fill = _fill(C_GOLD)

    # ── Tagline ───────────────────────────────────────────────────────────────
    _set_row_height(ws, AFTER_LOGO + 1, 22)
    ws.merge_cells(f"C{AFTER_LOGO+1}:F{AFTER_LOGO+1}")
    tl = ws[f"C{AFTER_LOGO+1}"]
    tl.value = "Sistem Laporan Keuangan Otomatis"
    tl.font  = Font(italic=True, size=12, color=C_GRAY, name="Arial")
    tl.fill  = _fill(C_DARK)
    tl.alignment = _align("center")

    # ── Kotak judul laporan ───────────────────────────────────────────────────
    BOX = AFTER_LOGO + 3
    for r in range(BOX, BOX + 5):
        _set_row_height(ws, r, 8 if r in (BOX, BOX + 4) else 36)
        for col in "CDEF":
            ws[f"{col}{r}"].fill = _fill(C_DARK2)

    ws.merge_cells(f"C{BOX+1}:F{BOX+1}")
    rt = ws[f"C{BOX+1}"]
    rt.value = "LAPORAN KEUANGAN"
    rt.font  = Font(bold=True, size=22, color=C_WHITE, name="Arial")
    rt.fill  = _fill(C_DARK2)
    rt.alignment = _align("center")

    ws.merge_cells(f"C{BOX+2}:F{BOX+2}")
    rp = ws[f"C{BOX+2}"]
    rp.value = f"PERIODE: {period_label.upper()}"
    rp.font  = Font(bold=True, size=14, color=C_GOLD, name="Arial")
    rp.fill  = _fill(C_DARK2)
    rp.alignment = _align("center")

    # ── Info cards: Mode & Tahun ──────────────────────────────────────────────
    CARD = BOX + 6
    _set_row_height(ws, CARD,     6)
    _set_row_height(ws, CARD + 1, 30)
    _set_row_height(ws, CARD + 2, 30)
    _set_row_height(ws, CARD + 3, 6)

    mode_label = "Bulanan" if mode == "monthly" else "Tahunan"
    cards = [
        ("C", "D", "MODE",  mode_label, C_BLUE),
        ("E", "F", "TAHUN", str(year),  C_GOLD),
    ]
    for c1, c2, lbl, val, accent in cards:
        for r in range(CARD, CARD + 4):
            ws[f"{c1}{r}"].fill = _fill(C_DARK2)
            ws[f"{c2}{r}"].fill = _fill(C_DARK2)
        # Accent top bar
        ws[f"{c1}{CARD}"].fill = _fill(accent)
        ws[f"{c2}{CARD}"].fill = _fill(accent)
        # Label + value
        ws.merge_cells(f"{c1}{CARD+1}:{c2}{CARD+1}")
        lc = ws[f"{c1}{CARD+1}"]
        lc.value = lbl
        lc.font  = Font(size=9, color=C_GRAY, name="Arial")
        lc.fill  = _fill(C_DARK2)
        lc.alignment = _align("center")

        ws.merge_cells(f"{c1}{CARD+2}:{c2}{CARD+2}")
        vc = ws[f"{c1}{CARD+2}"]
        vc.value = val
        vc.font  = Font(bold=True, size=14, color=C_WHITE, name="Arial")
        vc.fill  = _fill(C_DARK2)
        vc.alignment = _align("center")

    # ── Ringkasan angka ───────────────────────────────────────────────────────
    STAT = CARD + 5
    _section_header(ws, STAT, 3, 6, "Ringkasan Keuangan", height=24)
    _set_row_height(ws, STAT, 24)

    stats = [
        ("Total Pendapatan (Lunas)", total_pendapatan, C_GREEN),
        ("Total Pengeluaran",        total_pengeluaran, C_RED),
        ("Laba / Rugi Bersih",       total_laba,       C_ORANGE if total_laba >= 0 else "DC2626"),
    ]
    for i, (lbl, val, clr) in enumerate(stats):
        r = STAT + 1 + i
        _set_row_height(ws, r, 24)
        ws.merge_cells(f"C{r}:D{r}")
        lc = ws[f"C{r}"]
        lc.value = lbl
        lc.font  = Font(size=10, color=C_GRAY, name="Arial")
        lc.fill  = _fill(C_DARK2)
        lc.alignment = _align("left")

        ws.merge_cells(f"E{r}:F{r}")
        vc = ws[f"E{r}"]
        vc.value = f"Rp {int(val):,}".replace(",", ".")
        vc.font  = Font(bold=True, size=11, color=clr, name="Arial")
        vc.fill  = _fill(C_DARK2)
        vc.alignment = _align("right")

    # ── Gold bottom bar + footer ──────────────────────────────────────────────
    FOOT = STAT + len(stats) + 2
    _set_row_height(ws, FOOT, 4)
    for col in "BCDEFG":
        ws[f"{col}{FOOT}"].fill = _fill(C_GOLD)

    _set_row_height(ws, FOOT + 2, 20)
    ws.merge_cells(f"C{FOOT+2}:F{FOOT+2}")
    ft = ws[f"C{FOOT+2}"]
    ft.value = f"v1.0  ·  Digenerate: {generated_at}  ·  © Masashimura {year}"
    ft.font  = Font(italic=True, size=9, color=C_GRAY, name="Arial")
    ft.fill  = _fill(C_DARK)
    ft.alignment = _align("center")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2: ⚙ CONTROL PANEL
# ═══════════════════════════════════════════════════════════════════════════════

def _write_control_panel(wb, mode: str, month: int | None, year: int,
                          generated_at: str, period_label: str):
    ws = wb[SH_CTRL]
    _set_col_widths(ws, {"A": 2, "B": 28, "C": 22, "D": 36, "E": 2})

    _banner(ws, 1, 2, 4, "⚙  PARAMETER LAPORAN", bg=C_DARK3, size=14)

    _set_row_height(ws, 2, 22)
    ws.merge_cells("B2:D2")
    sub = ws["B2"]
    sub.value = "Konfigurasi periode dan cara generate laporan keuangan Masashimura"
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT)
    sub.alignment = _align("left")

    _set_row_height(ws, 3, 10)
    _section_header(ws, 4, 2, 4, "Parameter Aktif")

    params = [
        ("Mode Laporan",   "Bulanan" if mode == "monthly" else "Tahunan", C_BLUE,
         "monthly = rekap per hari | yearly = rekap per bulan"),
        ("Bulan",          str(month) if month else "—",                   C_BLUE,
         "Nomor bulan 1–12; wajib jika mode=monthly"),
        ("Tahun",          str(year),                                       C_BLUE,
         "Tahun laporan, 4-digit"),
        ("Periode",        period_label,                                    C_DARK,
         "Label yang tampil di seluruh laporan"),
        ("Digenerate",     generated_at,                                    C_GREEN,
         "✅ Otomatis dari timezone.now() saat endpoint dipanggil"),
    ]

    for i, (lbl, val, val_color, hint) in enumerate(params):
        r = 5 + i
        _set_row_height(ws, r, 26)
        bg = C_WHITE if i % 2 == 0 else C_STRIPE

        lc = ws.cell(r, 2, lbl)
        lc.font      = _font(bold=True, size=10)
        lc.fill      = _fill(bg)
        lc.alignment = _align("left")
        lc.border    = _border_thin()

        vc = ws.cell(r, 3, val)
        vc.font      = _font(bold=True, size=10, color=val_color)
        vc.fill      = _fill(bg)
        vc.alignment = _align("center")
        vc.border    = _border_thin()

        hc = ws.cell(r, 4, hint)
        hc.font      = _font(italic=True, size=9, color=C_GRAY)
        hc.fill      = _fill(bg)
        hc.alignment = _align("left", wrap=True)
        hc.border    = _border_thin()

    _set_row_height(ws, 11, 14)
    _section_header(ws, 12, 2, 4, "Cara Generate Laporan via API")

    endpoints = [
        ("Bulanan:", "GET /api/orders/export/finance-excel/?mode=monthly&month=6&year=2026"),
        ("Tahunan:", "GET /api/orders/export/finance-excel/?mode=yearly&year=2026"),
    ]
    for i, (prefix, url) in enumerate(endpoints):
        r = 13 + i * 2
        _set_row_height(ws, r, 20)
        _set_row_height(ws, r + 1, 24)

        ws.cell(r, 2, prefix).font = _font(bold=True, size=9, color=C_GRAY)
        ws.cell(r, 2).fill = _fill(C_LIGHT)
        ws.merge_cells(f"C{r}:D{r}")

        ws.merge_cells(f"B{r+1}:D{r+1}")
        uc = ws[f"B{r+1}"]
        uc.value = "  " + url
        uc.font  = Font(bold=True, size=9, name="Courier New", color=C_GOLD)
        uc.fill  = _fill(C_DARK)
        uc.alignment = _align("left")

    _set_row_height(ws, 17, 14)
    _section_header(ws, 18, 2, 4, "Catatan Teknis")

    notes = [
        "Tanggal 'Digenerate' diambil dari timezone.now() secara otomatis — tidak perlu diisi manual.",
        "Nama file otomatis: 'Rekap Finance Masashimura Juni 2026.xlsx'",
        "Logo diambil dari EXCEL_LOGO_PATH di settings.py (fallback ke teks jika tidak ada).",
        "Gunakan filter queryset Django sebelum memanggil export_finance_excel().",
    ]
    for i, note in enumerate(notes):
        r = 19 + i
        _set_row_height(ws, r, 22)
        bg = C_LIGHT if i % 2 == 0 else C_WHITE
        ws.merge_cells(f"B{r}:D{r}")
        nc = ws[f"B{r}"]
        nc.value = f"  ▸  {note}"
        nc.font  = _font(size=9, color=C_DARK)
        nc.fill  = _fill(bg)
        nc.alignment = _align("left")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3: 📊 REKAP PERIODE
# ═══════════════════════════════════════════════════════════════════════════════

def _write_rekap_periode(wb, mode: str, month: int | None, year: int,
                          orders_qs, expenses_qs, generated_at: str):
    ws = wb[SH_REKAP]
    _set_col_widths(ws, {"A": 2, "B": 18, "C": 22, "D": 22, "E": 22, "F": 2})

    period_str = f"{BULAN_ID[month]} {year}" if mode == "monthly" else f"Tahun {year}"
    _banner(ws, 1, 2, 5, f"📊  REKAP PERIODE — {period_str.upper()}", bg=C_BLUE)

    _set_row_height(ws, 2, 22)
    ws.merge_cells("B2:E2")
    sub = ws["B2"]
    sub.value = (
        f"Mode: {'Bulanan (per hari)' if mode == 'monthly' else 'Tahunan (per bulan)'}"
        f"  |  Digenerate: {generated_at}"
    )
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT)
    sub.alignment = _align("left")

    _set_row_height(ws, 3, 8)

    col_label = "Tanggal" if mode == "monthly" else "Bulan"
    headers = [col_label, "Pendapatan (Rp)", "Pengeluaran (Rp)", "Laba Bersih (Rp)"]
    _table_header(ws, 4, headers, start_col=2, height=28)
    ws.freeze_panes = "B5"

    DATA_START = 5

    if mode == "monthly":
        rev_qs = (
            orders_qs.filter(payment_status="paid")
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Sum("total_price"))
            .order_by("day")
        )
        exp_qs = (
            expenses_qs
            .values("date")
            .annotate(total=Sum("amount"))
        )
        rev_map = {str(r["day"]): float(r["total"] or 0) for r in rev_qs}
        exp_map = {str(e["date"]): float(e["total"] or 0) for e in exp_qs}

        days_in_month = calendar.monthrange(year, month)[1]
        rows = []
        for d in range(1, days_in_month + 1):
            date_str  = f"{year}-{month:02d}-{d:02d}"
            date_disp = f"{d:02d}/{month:02d}/{year}"
            rev = rev_map.get(date_str, 0)
            exp = exp_map.get(date_str, 0)
            rows.append((date_disp, rev, exp, rev - exp))
    else:
        rev_qs = (
            orders_qs.filter(payment_status="paid")
            .annotate(m=ExtractMonth("created_at"))
            .values("m")
            .annotate(total=Sum("total_price"))
            .order_by("m")
        )
        exp_qs = (
            expenses_qs
            .annotate(m=ExtractMonth("date"))
            .values("m")
            .annotate(total=Sum("amount"))
        )
        rev_map = {r["m"]: float(r["total"] or 0) for r in rev_qs}
        exp_map = {e["m"]: float(e["total"] or 0) for e in exp_qs}
        rows = [
            (BULAN_ID[m],
             rev_map.get(m, 0),
             exp_map.get(m, 0),
             rev_map.get(m, 0) - exp_map.get(m, 0))
            for m in range(1, 13)
        ]

    for i, (label, rev, exp, net) in enumerate(rows):
        r  = DATA_START + i
        bg = C_STRIPE if i % 2 == 0 else C_WHITE
        has_data = rev > 0 or exp > 0
        _set_row_height(ws, r, 20)

        lc = ws.cell(r, 2, label)
        lc.font      = _font(bold=has_data, color=C_BLUE if has_data else C_DARK)
        lc.fill      = _fill(C_BLUE_LT if has_data else bg)
        lc.alignment = _align("center")

        for ci, val in [(3, rev), (4, exp), (5, net)]:
            c = ws.cell(r, ci, val)
            c.number_format = FMT_RP
            c.alignment     = _align("right")
            if val == 0:
                c.font = _font(color="D1D5DB")
                c.fill = _fill(C_BLUE_LT if has_data else bg)
            elif ci == 5 and val < 0:
                c.font = _font(bold=True, color="DC2626")
                c.fill = _fill(C_RED_LT)
            elif ci == 5 and val > 0:
                c.font = _font(bold=True, color=C_GREEN)
                c.fill = _fill(C_GRN_LT)
            else:
                c.font = _font(bold=has_data)
                c.fill = _fill(C_BLUE_LT if has_data else bg)

    # TOTAL row
    total_r = DATA_START + len(rows)
    _set_row_height(ws, total_r, 28)
    t_rev = sum(r[1] for r in rows)
    t_exp = sum(r[2] for r in rows)
    t_net = t_rev - t_exp

    ws.cell(total_r, 2, "TOTAL").fill = _fill(C_DARK)
    ws.cell(total_r, 2).font      = _font(bold=True, size=11, color=C_WHITE)
    ws.cell(total_r, 2).alignment = _align("center")

    for ci, val, clr in [
        (3, t_rev, C_GOLD),
        (4, t_exp, C_GOLD),
        (5, t_net, C_GREEN if t_net >= 0 else "DC2626"),
    ]:
        c = ws.cell(total_r, ci, val)
        c.number_format = FMT_RP
        c.font      = _font(bold=True, size=11, color=clr)
        c.fill      = _fill(C_DARK)
        c.alignment = _align("right")

    # Keterangan warna
    _set_row_height(ws, total_r + 2, 8)
    _section_header(ws, total_r + 3, 2, 5, "📌  Keterangan Warna", height=24)
    legends = [
        (C_BLUE_LT, "Baris dengan data transaksi"),
        (C_GRN_LT,  "Laba bersih positif (untung)"),
        (C_RED_LT,  "Laba bersih negatif (rugi)"),
    ]
    for j, (bg, lbl) in enumerate(legends):
        r = total_r + 4 + j
        _set_row_height(ws, r, 20)
        ws.merge_cells(f"B{r}:E{r}")
        c = ws[f"B{r}"]
        c.value     = "  " + lbl
        c.font      = _font(size=9, color=C_GRAY)
        c.fill      = _fill(bg)
        c.alignment = _align("left")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4: 📋 RINGKASAN
# ═══════════════════════════════════════════════════════════════════════════════

def _write_ringkasan(wb, period_label: str, generated_at: str,
                      orders_qs, expenses_qs):
    ws = wb[SH_RING]
    _set_col_widths(ws, {"A": 2, "B": 30, "C": 2, "D": 26, "E": 2})

    _banner(ws, 1, 2, 4, "📋  RINGKASAN KEUANGAN", bg=C_GREEN)

    _set_row_height(ws, 2, 22)
    ws.merge_cells("B2:D2")
    sub = ws["B2"]
    sub.value = f"Periode: {period_label}  |  Digenerate: {generated_at}"
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT)
    sub.alignment = _align("left")

    _set_row_height(ws, 3, 10)

    # ── Hitung nilai ringkasan dari queryset ──────────────────────────────────
    paid_orders  = orders_qs.filter(payment_status="paid")
    total_rev    = float(paid_orders.aggregate(t=Sum("total_price"))["t"] or 0)
    count_paid   = paid_orders.count()
    count_all    = orders_qs.count()
    count_pending = orders_qs.exclude(payment_status="paid").count()
    avg_order    = (total_rev / count_paid) if count_paid else 0
    total_exp    = float(expenses_qs.aggregate(t=Sum("amount"))["t"] or 0)
    net          = total_rev - total_exp
    margin       = (net / total_rev * 100) if total_rev else 0

    count_cash   = orders_qs.filter(payment_method="cash").count()
    count_qris   = orders_qs.filter(payment_method__icontains="qris").count()
    count_web    = orders_qs.filter(source="web").count()
    count_pos    = orders_qs.filter(source="pos").count()

    # ── KPI Cards: 3 besar ───────────────────────────────────────────────────
    kpis = [
        ("💰 PENDAPATAN (LUNAS)", f"Rp {int(total_rev):,}".replace(",", "."),
         "Total pendapatan dari order lunas", C_GREEN, C_GRN_LT),
        ("🛒 PENGELUARAN", f"Rp {int(total_exp):,}".replace(",", "."),
         "Total biaya operasional periode ini", C_RED, C_RED_LT),
        ("📈 LABA BERSIH", f"Rp {int(net):,}".replace(",", "."),
         "Pendapatan dikurangi pengeluaran",
         C_GREEN if net >= 0 else "DC2626",
         C_GRN_LT if net >= 0 else C_RED_LT),
    ]

    for i, (title, val_text, sub_text, accent, bg_lt) in enumerate(kpis):
        base = 4 + i * 6
        _set_row_height(ws, base,     5)      # accent bar
        _set_row_height(ws, base + 1, 22)     # title
        _set_row_height(ws, base + 2, 44)     # big value
        _set_row_height(ws, base + 3, 20)     # subtitle
        _set_row_height(ws, base + 4, 8)      # spacer

        ws.merge_cells(f"B{base}:D{base}")
        ws[f"B{base}"].fill = _fill(accent)

        ws.merge_cells(f"B{base+1}:D{base+1}")
        tc = ws[f"B{base+1}"]
        tc.value = title;  tc.font = _font(bold=True, size=11, color=accent)
        tc.fill  = _fill(bg_lt);  tc.alignment = _align("left")

        ws.merge_cells(f"B{base+2}:D{base+2}")
        vc = ws[f"B{base+2}"]
        vc.value = val_text
        vc.font  = Font(bold=True, size=22, color=accent, name="Arial Black")
        vc.fill  = _fill(bg_lt);  vc.alignment = _align("center")

        ws.merge_cells(f"B{base+3}:D{base+3}")
        sc = ws[f"B{base+3}"]
        sc.value = sub_text;  sc.font = _font(italic=True, size=9, color=C_GRAY)
        sc.fill  = _fill(bg_lt);  sc.alignment = _align("center")

    # ── Tabel metrik detail ───────────────────────────────────────────────────
    MET = 4 + 3 * 6 + 1
    _section_header(ws, MET, 2, 4, "📊  Detail Metrik")
    metrics = [
        ("Jumlah Order Lunas",        f"{count_paid} order"),
        ("Jumlah Order Pending",       f"{count_pending} order"),
        ("Rata-rata Nilai per Order",  f"Rp {int(avg_order):,}".replace(",", ".")),
        ("Margin Laba",               f"{margin:.2f}%"),
        ("Transaksi Cash",            f"{count_cash} transaksi"),
        ("Transaksi QRIS",            f"{count_qris} transaksi"),
        ("Order dari Web",            f"{count_web} order"),
        ("Order dari POS",            f"{count_pos} order"),
    ]
    for i, (lbl, val) in enumerate(metrics):
        r  = MET + 1 + i
        bg = C_WHITE if i % 2 == 0 else C_STRIPE
        _set_row_height(ws, r, 24)

        is_neg = val.startswith("-") or val.startswith("Rp -")
        val_color = "DC2626" if is_neg else (C_GREEN if "Rp" in val and not is_neg else C_BLUE)

        lc = ws.cell(r, 2, lbl)
        lc.font = _font(size=10); lc.fill = _fill(bg)
        lc.alignment = _align("left"); lc.border = _border_thin()

        vc = ws.cell(r, 4, val)
        vc.font = _font(bold=True, size=10, color=val_color)
        vc.fill = _fill(bg); vc.alignment = _align("right"); vc.border = _border_thin()

    # ── Panduan baca laporan ──────────────────────────────────────────────────
    GUIDE = MET + 1 + len(metrics) + 2
    _section_header(ws, GUIDE, 2, 4, "💡  Cara Membaca Laporan Ini")
    guides = [
        "📊 Rekap Periode  →  Pendapatan & pengeluaran per hari atau per bulan",
        "📄 Detail Transaksi  →  Semua order dengan status, metode, dan nominal",
        "🍜 Top Menu  →  Menu terlaris berdasarkan qty dan omzet",
        "💰 Pengeluaran  →  Detail biaya operasional per kategori",
        "⚙ Control Panel  →  Cara generate laporan untuk periode lain",
    ]
    for i, text in enumerate(guides):
        r  = GUIDE + 1 + i
        bg = C_LIGHT if i % 2 == 0 else C_WHITE
        _set_row_height(ws, r, 22)
        ws.merge_cells(f"B{r}:D{r}")
        c = ws[f"B{r}"]
        c.value = "  " + text; c.font = _font(size=10)
        c.fill  = _fill(bg);   c.alignment = _align("left")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 5: 📄 DETAIL TRANSAKSI
# ═══════════════════════════════════════════════════════════════════════════════

def _write_detail_transaksi(wb, orders_qs, period_label: str, generated_at: str):
    ws = wb[SH_DETAIL]
    _set_col_widths(ws, {
        "A": 5, "B": 20, "C": 14, "D": 8, "E": 14,
        "F": 14, "G": 14, "H": 11, "I": 14, "J": 11,
        "K": 15, "L": 9, "M": 18,
    })

    orders_list = list(orders_qs.order_by("-created_at"))
    _banner(ws, 1, 1, 13, "📄  DETAIL TRANSAKSI", bg=C_ORANGE)

    _set_row_height(ws, 2, 22)
    ws.merge_cells("A2:M2")
    sub = ws["A2"]
    sub.value = (
        f"Periode: {period_label}  |  {len(orders_list)} transaksi"
        f"  |  Digenerate: {generated_at}"
    )
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT);  sub.alignment = _align("left")

    _set_row_height(ws, 3, 8)

    headers = ["No","No. Order","Tanggal","Waktu","Nama","HP",
               "Subtotal","Diskon","Total","Status","Metode","Source","Catatan"]
    _table_header(ws, 4, headers, start_col=1)

    STATUS_STYLE = {
        "paid":    (C_GRN_LT, C_GREEN),
        "Lunas":   (C_GRN_LT, C_GREEN),
        "pending": (C_YLW_LT, C_ORANGE),
        "unpaid":  (C_YLW_LT, C_ORANGE),
        "Pending": (C_YLW_LT, C_ORANGE),
    }

    DATA_START = 5
    for idx, order in enumerate(orders_list, 1):
        r  = DATA_START + idx - 1
        _set_row_height(ws, r, 22)
        status_raw = order.payment_status
        status_lbl = _map_status(status_raw)
        row_bg, status_fg = STATUS_STYLE.get(status_raw, (C_STRIPE, C_GRAY))

        data = [
            (1,  idx,                           False, FMT_INT,  "center"),
            (2,  order.order_number,             True,  None,     "left"),
            (3,  order.created_at.strftime("%d/%m/%Y"), False, None, "center"),
            (4,  order.created_at.strftime("%H:%M"),    False, None, "center"),
            (5,  order.customer_name or "—",     False, None,     "left"),
            (6,  order.customer_phone or "—",    False, None,     "left"),
            (7,  float(order.subtotal),          False, FMT_RP,   "right"),
            (8,  float(order.discount_amount),   False, FMT_RP,   "right"),
            (9,  float(order.total_price),       True,  FMT_RP,   "right"),
            (10, status_lbl,                     True,  None,     "center"),
            (11, order.payment_method or "—",    False, None,     "center"),
            (12, _map_source(order.source),      False, None,     "center"),
            (13, order.notes or "",              False, None,     "left"),
        ]
        for col_n, val, bold, fmt, align_h in data:
            c = ws.cell(r, col_n, val)
            c.fill      = _fill(row_bg)
            c.alignment = _align(align_h)
            c.border    = _border_bottom()
            if col_n == 10:
                c.font = _font(bold=True, color=status_fg)
            else:
                c.font = _font(bold=bold)
            if fmt:
                c.number_format = fmt

    # Summary bar
    last_r = DATA_START + len(orders_list)
    _set_row_height(ws, last_r + 1, 26)
    paid_total = float(
        orders_list and
        sum(float(o.total_price) for o in orders_list if o.payment_status == "paid")
        or 0
    )
    count_paid = sum(1 for o in orders_list if o.payment_status == "paid")
    count_pend = sum(1 for o in orders_list if o.payment_status != "paid")

    ws.merge_cells(f"A{last_r+1}:F{last_r+1}")
    sc = ws[f"A{last_r+1}"]
    sc.value = (
        f"  Total: {len(orders_list)} transaksi"
        f"  |  Lunas: {count_paid}"
        f"  |  Pending: {count_pend}"
    )
    sc.font  = _font(bold=True, size=10, color=C_WHITE)
    sc.fill  = _fill(C_DARK2);  sc.alignment = _align("left")

    for ci in range(7, 14):
        ws.cell(last_r + 1, ci).fill = _fill(C_DARK2)

    ws.cell(last_r + 1, 8, "Total Omzet Lunas:").font = _font(bold=True, color=C_GOLD)
    ws.cell(last_r + 1, 8).fill = _fill(C_DARK2)
    ws.cell(last_r + 1, 8).alignment = _align("right")

    tc = ws.cell(last_r + 1, 9, paid_total)
    tc.number_format = FMT_RP
    tc.font      = _font(bold=True, size=11, color=C_GOLD)
    tc.fill      = _fill(C_DARK2);  tc.alignment = _align("right")

    if len(orders_list):
        ws.auto_filter.ref = f"A4:M{DATA_START + len(orders_list) - 1}"


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 6: 🍜 TOP MENU
# ═══════════════════════════════════════════════════════════════════════════════

def _write_top_menu(wb, orders_qs, days_in_period: int,
                    period_label: str, generated_at: str):
    ws = wb[SH_TOPMENU]
    _set_col_widths(ws, {"A": 2, "B": 7, "C": 28, "D": 14, "E": 12, "F": 14, "G": 16, "H": 2})

    _banner(ws, 1, 2, 7, "🍜  TOP MENU — TERLARIS", bg="DC2626")

    _set_row_height(ws, 2, 22)
    ws.merge_cells("B2:G2")
    sub = ws["B2"]
    sub.value = f"Berdasarkan qty terjual  |  Periode: {period_label}  |  Digenerate: {generated_at}"
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT);  sub.alignment = _align("left")

    _set_row_height(ws, 3, 8)

    menus = (
        OrderItem.objects.filter(order__in=orders_qs)
        .values("menu__name")
        .annotate(
            qty=Sum("quantity"),
            omzet=Sum(
                ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField())
            ),
        )
        .order_by("-qty")
    )
    menus_list  = list(menus)
    total_omzet = sum(float(m["omzet"] or 0) for m in menus_list)
    total_qty   = sum(m["qty"] or 0 for m in menus_list)

    headers = ["Rank","Nama Menu","Omzet (Rp)","Qty","% Kontribusi","Rata-rata/hari"]
    _table_header(ws, 4, headers, start_col=2, height=26)
    ws.freeze_panes = None  # no freeze for this sheet

    RANK_ICONS = ["🥇","🥈","🥉"]
    RANK_BGS   = [C_YLW_LT, C_STRIPE, C_RED_LT]

    DATA_START = 5
    for i, item in enumerate(menus_list):
        r   = DATA_START + i
        _set_row_height(ws, r, 26)
        rank = RANK_ICONS[i] if i < 3 else str(i + 1)
        omzet = float(item["omzet"] or 0)
        qty   = item["qty"] or 0
        pct   = omzet / total_omzet if total_omzet else 0
        avg   = round(qty / days_in_period, 1) if days_in_period else 0
        bg    = RANK_BGS[i] if i < 3 else (C_STRIPE if i % 2 == 0 else C_WHITE)

        data = [
            (2, rank,              True,  None,    "center"),
            (3, item["menu__name"],True if i==0 else False, None, "left"),
            (4, omzet,             False, FMT_RP,  "right"),
            (5, qty,               False, FMT_INT, "center"),
            (6, pct,               False, FMT_PCT, "right"),
            (7, avg,               False, "0.0",   "center"),
        ]
        for col_n, val, bold, fmt, align_h in data:
            c = ws.cell(r, col_n, val)
            c.fill      = _fill(bg)
            c.alignment = _align(align_h)
            c.border    = _border_bottom()
            fg = C_GOLD if i == 0 else C_DARK
            c.font      = _font(bold=bold, color=fg)
            if fmt:
                c.number_format = fmt

    # TOTAL
    total_r = DATA_START + len(menus_list)
    _set_row_height(ws, total_r, 26)
    for col in range(2, 8):
        ws.cell(total_r, col).fill = _fill(C_DARK)
    ws.cell(total_r, 2, "TOTAL").font = _font(bold=True, size=11, color=C_WHITE)
    ws.cell(total_r, 2).alignment = _align("center")

    ws.cell(total_r, 4, total_omzet)
    ws.cell(total_r, 4).number_format = FMT_RP
    ws.cell(total_r, 4).font = _font(bold=True, size=11, color=C_GOLD)
    ws.cell(total_r, 4).alignment = _align("right")

    ws.cell(total_r, 5, total_qty)
    ws.cell(total_r, 5).font = _font(bold=True, size=11, color=C_GOLD)
    ws.cell(total_r, 5).alignment = _align("center")

    ws.cell(total_r, 6, 1.0)
    ws.cell(total_r, 6).number_format = FMT_PCT
    ws.cell(total_r, 6).font = _font(bold=True, size=11, color=C_GOLD)
    ws.cell(total_r, 6).alignment = _align("right")

    # Insight
    if menus_list:
        best_qty = max(menus_list, key=lambda x: x["qty"] or 0)
        best_rev = max(menus_list, key=lambda x: float(x["omzet"] or 0))
        ins_r = total_r + 2
        _section_header(ws, ins_r, 2, 7, "💡  Insight Otomatis")
        insights = [
            f"Menu terlaris (qty): {best_qty['menu__name']} — {best_qty['qty']} pcs terjual",
            f"Menu omzet tertinggi: {best_rev['menu__name']} — Rp {int(float(best_rev['omzet'] or 0)):,}".replace(",","."),
            f"Total menu terjual: {total_qty} pcs  |  Total omzet: Rp {int(total_omzet):,}".replace(",","."),
        ]
        for j, text in enumerate(insights):
            r  = ins_r + 1 + j
            _set_row_height(ws, r, 22)
            ws.merge_cells(f"B{r}:G{r}")
            c = ws[f"B{r}"]
            c.value = "  ▸  " + text
            c.font  = _font(size=10)
            c.fill  = _fill(C_LIGHT if j % 2 == 0 else C_WHITE)
            c.alignment = _align("left")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 7: 💰 PENGELUARAN
# ═══════════════════════════════════════════════════════════════════════════════

def _write_pengeluaran(wb, expenses_qs, period_label: str, generated_at: str):
    ws = wb[SH_EXPENSE]
    _set_col_widths(ws, {"A": 2, "B": 6, "C": 14, "D": 18, "E": 28, "F": 18, "G": 14, "H": 22, "I": 2})

    expenses_list = list(expenses_qs.order_by("date"))
    _banner(ws, 1, 2, 8, "💰  PENGELUARAN", bg=C_PURPLE)

    _set_row_height(ws, 2, 22)
    ws.merge_cells("B2:H2")
    sub = ws["B2"]
    sub.value = (
        f"Periode: {period_label}  |  {len(expenses_list)} item"
        f"  |  Digenerate: {generated_at}"
    )
    sub.font  = _font(italic=True, size=10, color=C_GRAY)
    sub.fill  = _fill(C_LIGHT);  sub.alignment = _align("left")

    _set_row_height(ws, 3, 8)

    headers = ["No","Tanggal","Kategori","Keterangan","Nominal (Rp)","Metode","Catatan"]
    _table_header(ws, 4, headers, start_col=2, height=26)

    CAT_STYLE = {
        "Operasional": (C_YLW_LT,    C_ORANGE),
        "Bahan Baku":  (C_GRN_LT,    C_GREEN),
        "Karyawan":    (C_BLUE_LT,   C_BLUE),
        "Marketing":   ("F3E8FF",    C_PURPLE),
    }

    DATA_START = 5
    for i, exp in enumerate(expenses_list):
        r   = DATA_START + i
        _set_row_height(ws, r, 22)
        cat  = getattr(exp, "category", "Operasional")
        bg, fg = CAT_STYLE.get(cat, (C_STRIPE, C_DARK))

        data = [
            (2, i + 1,                           False, None,    "center"),
            (3, exp.date.strftime("%d/%m/%Y"),   False, None,    "center"),
            (4, cat,                              True,  None,    "left"),
            (5, exp.description,                  False, None,    "left"),
            (6, float(exp.amount),               True,  FMT_RP,  "right"),
            (7, getattr(exp, "payment_method", "Cash"), False, None, "center"),
            (8, getattr(exp, "notes", "") or "", False, None,    "left"),
        ]
        for col_n, val, bold, fmt, align_h in data:
            c = ws.cell(r, col_n, val)
            c.fill      = _fill(bg)
            c.alignment = _align(align_h)
            c.border    = _border_bottom()
            c.font      = _font(bold=bold, color=fg if col_n == 4 else C_DARK)
            if fmt:
                c.number_format = fmt

    # TOTAL
    total_exp   = float(expenses_qs.aggregate(t=Sum("amount"))["t"] or 0)
    last_data_r = DATA_START + len(expenses_list) - 1
    total_r     = last_data_r + 2
    _set_row_height(ws, total_r, 28)

    ws.merge_cells(f"B{total_r}:E{total_r}")
    tc = ws[f"B{total_r}"]
    tc.value = "  TOTAL PENGELUARAN"
    tc.font  = _font(bold=True, size=11, color=C_WHITE)
    tc.fill  = _fill(C_DARK);  tc.alignment = _align("left")

    vc = ws.cell(total_r, 6, total_exp)
    vc.number_format = FMT_RP
    vc.font      = _font(bold=True, size=12, color=C_GOLD)
    vc.fill      = _fill(C_DARK);  vc.alignment = _align("right")
    for col in [7, 8]:
        ws.cell(total_r, col).fill = _fill(C_DARK)

    # Rekap per kategori
    rekap_r = total_r + 3
    _section_header(ws, rekap_r, 2, 8, "📊  REKAP PENGELUARAN PER KATEGORI")

    cat_headers = ["Kategori", "Total (Rp)", "% dari Total", "Status"]
    _set_row_height(ws, rekap_r + 1, 24)
    for i, (col_n, h) in enumerate(zip([2, 6, 8, 4], cat_headers)):
        c = ws.cell(rekap_r + 1, col_n, h)
        c.font = _font(bold=True, color=C_WHITE)
        c.fill = _fill(C_DARK2);  c.alignment = _align("center")

    # Ambil kategori dari DB
    try:
        db_cats = list(expenses_qs.values_list("category", flat=True).distinct())
    except Exception:
        db_cats = []
    all_cats = list(dict.fromkeys(db_cats + ["Bahan Baku", "Operasional", "Karyawan", "Marketing"]))

    # Aggregate per kategori
    cat_totals = {}
    for exp in expenses_list:
        cat = getattr(exp, "category", "Operasional")
        cat_totals[cat] = cat_totals.get(cat, 0) + float(exp.amount)

    for i, cat in enumerate(all_cats):
        r    = rekap_r + 2 + i
        _set_row_height(ws, r, 22)
        bg, fg = CAT_STYLE.get(cat, (C_STRIPE, C_DARK))
        amt  = cat_totals.get(cat, 0)
        pct  = amt / total_exp if total_exp and amt else 0

        ws.merge_cells(f"B{r}:E{r}")
        lc = ws[f"B{r}"]
        lc.value = cat;  lc.font = _font(bold=True, color=fg)
        lc.fill  = _fill(bg);  lc.alignment = _align("left")

        vc = ws.cell(r, 6, amt)
        vc.number_format = FMT_RP
        vc.font      = _font(bold=True, color=C_GREEN if amt == 0 else C_DARK)
        vc.fill      = _fill(bg);  vc.alignment = _align("right")

        pc = ws.cell(r, 8, pct)
        pc.number_format = FMT_PCT
        pc.font  = _font(color=C_GRAY);  pc.fill = _fill(bg)
        pc.alignment = _align("right")

        st = ws.cell(r, 4, "—" if amt == 0 else "✓ Ada data")
        st.font  = _font(size=9, color=C_GRAY if amt == 0 else C_GREEN)
        st.fill  = _fill(bg);  st.alignment = _align("center")


# ═══════════════════════════════════════════════════════════════════════════════
# FUNGSI UTAMA — dipanggil dari view Django
# ═══════════════════════════════════════════════════════════════════════════════

def export_finance_excel(
    request,
    orders_qs,
    expenses_qs,
    period_label: str,
    mode: str = "monthly",
    month: int | None = None,
    year: int | None = None,
) -> HttpResponse:
    """
    Ekspor laporan keuangan ke Excel.

    Nama file otomatis:
      - Bulanan : 'Rekap Finance Masashimura Juni 2026.xlsx'
      - Tahunan : 'Rekap Finance Masashimura Tahun 2026.xlsx'

    Tanggal 'Digenerate' diambil secara otomatis dari timezone.now()
    SAAT fungsi ini dipanggil — tidak perlu di-hardcode.

    Parameters
    ----------
    request       : Django HttpRequest
    orders_qs     : QuerySet Order (sudah difilter periode)
    expenses_qs   : QuerySet Expense (sudah difilter periode)
    period_label  : Label teks, mis. 'Juni 2026' / 'Tahun 2026'
    mode          : 'monthly' | 'yearly'
    month         : 1–12, wajib jika mode='monthly'
    year          : 4-digit year
    """
    now = timezone.now()
    if year is None:
        year = now.year
    if mode == "monthly" and month is None:
        month = now.month

    # ── Tanggal generate — otomatis saat dipanggil ────────────────────────────
    generated_at = _now_label()
    filename     = _build_filename(mode, month, year)

    days_in_period = calendar.monthrange(year, month)[1] if mode == "monthly" else 365

    # ── Hitung ringkasan untuk cover ─────────────────────────────────────────
    total_rev = float(
        orders_qs.filter(payment_status="paid")
        .aggregate(t=Sum("total_price"))["t"] or 0
    )
    total_exp = float(expenses_qs.aggregate(t=Sum("amount"))["t"] or 0)
    total_net = total_rev - total_exp

    # ── Bangun workbook ──────────────────────────────────────────────────────
    wb = _create_workbook()

    _write_control_panel(wb, mode, month, year, generated_at, period_label)
    _write_rekap_periode(wb, mode, month, year, orders_qs, expenses_qs, generated_at)
    _write_ringkasan(wb, period_label, generated_at, orders_qs, expenses_qs)
    _write_detail_transaksi(wb, orders_qs, period_label, generated_at)
    _write_top_menu(wb, orders_qs, days_in_period, period_label, generated_at)
    _write_pengeluaran(wb, expenses_qs, period_label, generated_at)
    _write_cover(wb, period_label, generated_at, mode, year,
                 total_rev, total_exp, total_net)

    wb.active = wb[SH_RING]

    # ── HTTP response ─────────────────────────────────────────────────────────
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    encoded  = filename.encode("utf-8").decode("latin-1", errors="replace")
    response["Content-Disposition"] = (
        f'attachment; filename="{encoded}"; '
        f"filename*=UTF-8''{filename.replace(' ', '%20')}"
    )
    wb.save(response)
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW HELPER — daftarkan di urls.py
# ═══════════════════════════════════════════════════════════════════════════════

def export_finance_excel_view(request) -> HttpResponse:
    """
    GET /api/orders/export/finance-excel/?mode=monthly&month=6&year=2026
    GET /api/orders/export/finance-excel/?mode=yearly&year=2026

    Tanggal generate di-set otomatis — tidak perlu query param tambahan.
    """
    now   = timezone.now()
    mode  = request.GET.get("mode", "monthly")
    year  = int(request.GET.get("year",  now.year))
    month = int(request.GET.get("month", now.month)) if mode == "monthly" else None

    if mode == "monthly":
        orders_qs   = Order.objects.filter(
            created_at__year=year, created_at__month=month
        ).prefetch_related("items__menu")
        expenses_qs = Expense.objects.filter(date__year=year, date__month=month)
        period_label = f"{BULAN_ID[month]} {year}"
    else:
        orders_qs   = Order.objects.filter(created_at__year=year).prefetch_related("items__menu")
        expenses_qs = Expense.objects.filter(date__year=year)
        period_label = f"Tahun {year}"

    return export_finance_excel(
        request=request,
        orders_qs=orders_qs,
        expenses_qs=expenses_qs,
        period_label=period_label,
        mode=mode,
        month=month,
        year=year,
    )
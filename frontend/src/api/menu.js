import apiClient from "./client";

export const menuAPI = {
  getAll: () => apiClient.get("/menus/"),
  create: (formData) =>
    apiClient.post("/menus/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  update: (id, formData) =>
    apiClient.put(`/menus/${id}/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  delete: (id) => apiClient.delete(`/menus/${id}/`),
};

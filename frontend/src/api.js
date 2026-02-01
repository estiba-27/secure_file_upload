// src/api.js
const BASE_URL = "http://localhost:8000";

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });
  return res.json();
}

export async function fetchFiles() {
  const res = await fetch(`${BASE_URL}/files`);
  return res.json();
}


import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const API_URL = "http://localhost:8000/api";

  // Convert bytes to MB with 2 decimal places
  const formatSizeMB = (bytes) => (bytes / (1024 * 1024)).toFixed(2);

  // Fetch uploaded files
  const fetchFiles = async () => {
    try {
      const res = await axios.get(`${API_URL}/files`);
      setFiles(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // Automatic refresh every 5 seconds
  useEffect(() => {
    fetchFiles();
    const interval = setInterval(fetchFiles, 5000);
    return () => clearInterval(interval);
  }, []);

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle file upload
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setMessage(
        `File "${res.data.filename}" uploaded successfully! Size: ${formatSizeMB(res.data.size)} MB`
      );
      setFile(null);
      fetchFiles(); // Refresh immediately after upload
    } catch (err) {
      console.error(err);
      setMessage("Upload failed. Check console for details.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1>Secure File Upload</h1>

      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {message && <p>{message}</p>}

      <h2>Uploaded Files</h2>
      <table border="1" cellPadding="5" cellSpacing="0">
        <thead>
          <tr>
            <th>Filename</th>
            <th>Size (MB)</th>
            <th>Hash</th>
            <th>Status</th>
            <th>Reason</th>
            <th>Uploaded At</th>
          </tr>
        </thead>
        <tbody>
          {files.length === 0 ? (
            <tr>
              <td colSpan="6">No files uploaded yet.</td>
            </tr>
          ) : (
            files.map((f, idx) => (
              <tr key={idx}>
                <td>{f.filename}</td>
                <td>{formatSizeMB(f.size)}</td>
                <td>{f.hash}</td>
                <td style={{ color: f.status === "accepted" ? "green" : "red" }}>
                  {f.status}
                </td>
                <td>{f.reason || "-"}</td>
                <td>{new Date(f.uploaded_at).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;


import React, { useState, useEffect } from "react";
import UploadForm from "./components/FileUpload";
import FileTable from "./components/FileTable";
import axios from "axios";

function App() {
  const [files, setFiles] = useState([]);
  const API_URL = "http://localhost:8000/api";

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

  return (
    <div>
      <h1>Secure File Upload</h1>
      <UploadForm onUpload={fetchFiles} />
      <FileTable files={files} />
    </div>
  );
}

export default App;


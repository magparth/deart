import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [gallery, setGallery] = useState([]);

  const generateImage = async () => {
    if (!prompt) return;
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/generate", {
        prompt,
      });
      setImageUrl(response.data.image_url);
      setGallery((prev) => [response.data.image_url, ...prev]); // Add to gallery
    } catch (error) {
      console.error("Error generating image:", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white p-6">
      <div className="max-w-3xl mx-auto flex flex-col items-center">
        <h1 className="text-4xl font-extrabold text-purple-400 drop-shadow-md mb-8">🎨 AI Art Mint</h1>

        <input
          type="text"
          placeholder="Enter your creative prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full max-w-xl p-3 rounded-xl border border-purple-600 bg-black text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <button
          onClick={generateImage}
          className="mt-4 px-6 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 transition-all shadow-md hover:shadow-purple-500/50"
        >
          {loading ? "Generating..." : "Generate Image"}
        </button>

        {imageUrl && !loading && (
          <div className="mt-10">
            <h2 className="text-xl mb-4">Latest Generation:</h2>
            <img
              src={imageUrl}
              alt="Generated"
              className="rounded-xl shadow-lg border border-purple-700"
            />
          </div>
        )}

        {gallery.length > 0 && (
          <div className="mt-12 w-full">
            <h2 className="text-2xl font-semibold mb-4 text-purple-400">🖼️ Gallery</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {gallery.map((url, index) => (
                <img
                  key={index}
                  src={url}
                  alt={`Generated ${index}`}
                  className="rounded-lg border border-gray-700 hover:scale-105 transition-transform"
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

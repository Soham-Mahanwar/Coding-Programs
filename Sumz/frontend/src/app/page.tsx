"use client";
import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function Home() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setSummary("");
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/summarize?url=${url}`
      );
      setSummary(response.data.summary);
    } catch (error) {
      console.error(error);
      setSummary("Failed to summarize the video.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900 text-white">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <h1 className="text-5xl font-bold mb-4">
          <motion.span
            initial={{ x: -100 }}
            animate={{ x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Sumz
          </motion.span>
        </h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="text-lg text-gray-400"
        >
          Get the summary of any YouTube video in seconds.
        </motion.p>
      </motion.div>

      <form onSubmit={handleSubmit} className="mt-8 w-full max-w-md">
        <div className="flex items-center border-b-2 border-teal-500 py-2">
          <input
            className="appearance-none bg-transparent border-none w-full text-gray-300 mr-3 py-1 px-2 leading-tight focus:outline-none"
            type="text"
            placeholder="Enter YouTube URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            className="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded"
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? "Summarizing..." : "Summarize"}
          </button>
        </div>
      </form>

      {summary && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-8 p-6 bg-gray-800 rounded-lg w-full max-w-md"
        >
          <h2 className="text-2xl font-bold mb-4">Summary</h2>
          <p className="text-gray-300">{summary}</p>
        </motion.div>
      )}
    </main>
  );
}

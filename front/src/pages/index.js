import { useState, useCallback } from "react";
import Head from "next/head";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const MAX_RETRIES = 3;

export default function Home() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isRetrying, setIsRetrying] = useState(false);
  const [copied, setCopied] = useState(false);
  const [urlError, setUrlError] = useState("");
  const [expiresIn, setExpiresIn] = useState(null);

  const validateUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const fetchWithRetry = useCallback(
    async (url, options, retries = MAX_RETRIES) => {
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response;
      } catch (error) {
        if (retries > 0) {
          setIsRetrying(true);
          await new Promise((resolve) =>
            setTimeout(resolve, Math.pow(2, MAX_RETRIES - retries) * 1000),
          );
          return fetchWithRetry(url, options, retries - 1);
        }
        throw error;
      } finally {
        setIsRetrying(false);
      }
    },
    [],
  );

  const handleUrlChange = (e) => {
    const url = e.target.value;
    setLongUrl(url);
    if (url && !validateUrl(url)) {
      setUrlError("Please enter a valid URL (e.g., https://example.com)");
    } else {
      setUrlError("");
    }
  };

  const formatTimeRemaining = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    return `${hours} ${hours === 1 ? "hour" : "hours"}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateUrl(longUrl)) {
      setUrlError("Please enter a valid URL (e.g., https://example.com)");
      return;
    }

    setIsLoading(true);
    setError("");
    setShortUrl("");
    setCopied(false);
    setExpiresIn(null);

    try {
      const response = await fetchWithRetry(`${API_URL}/shorten`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ long_url: longUrl }),
      });

      const data = await response.json();
      setShortUrl(data.short_url);
      setExpiresIn(data.expires_in);
    } catch (error) {
      setError("Error shortening URL. Please try again.");
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      setCopied(true);
      // Reset the "Copied" state after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
      setError("Failed to copy to clipboard");
    }
  };

  return (
    <>
      <Head>
        <title>RiShort</title>
        <meta
          name="description"
          content="Transform long URLs into short, shareable links"
        />
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-purple-100 flex items-center justify-center p-6">
        <div className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-8">
          <div className="text-center mb-10">
            <h1 className="text-5xl font-extrabold text-gray-900 mb-4">
              RiShort
            </h1>
            <p className="text-lg text-gray-700">
              Transform long URLs into short, shareable links
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="url"
                className="block text-base font-medium text-gray-800 mb-2"
              >
                Enter your URL
              </label>
              <input
                type="url"
                id="url"
                required
                placeholder="https://example.com/your-long-url"
                className={`w-full px-4 py-3 rounded-lg border ${
                  urlError
                    ? "border-red-500 focus:ring-red-500"
                    : "border-gray-300 focus:ring-purple-500"
                } focus:border-purple-500 text-gray-800 outline-none transition-all duration-200 shadow-sm`}
                value={longUrl}
                onChange={handleUrlChange}
              />
              {urlError && (
                <p className="mt-2 text-sm text-red-600">{urlError}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading || !!urlError}
              className={`w-full py-3 rounded-lg text-white font-medium transition-all duration-200 ease-in-out transform ${
                isLoading || !!urlError
                  ? "bg-purple-300 cursor-not-allowed"
                  : "bg-purple-600 hover:bg-purple-700 hover:-translate-y-0.5 hover:shadow-lg"
              }`}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  {isRetrying ? "Retrying..." : "Shortening..."}
                  <svg
                    className="animate-spin ml-2 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                </span>
              ) : (
                "Shorten URL"
              )}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 rounded-lg border border-red-200">
              <p className="text-red-600 text-sm text-center font-medium">
                {error}
              </p>
            </div>
          )}

          {shortUrl && (
            <div className="mt-8 p-5 bg-gray-50 rounded-xl border border-gray-200 shadow-sm">
              <p className="text-base font-semibold text-gray-700 mb-3">
                Your shortened URL:
              </p>
              <div className="flex items-center space-x-3 mb-3">
                <input
                  type="text"
                  readOnly
                  value={shortUrl}
                  className="flex-1 px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-800 shadow-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
                <button
                  onClick={copyToClipboard}
                  className={`px-5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ease-in-out ${
                    copied
                      ? "bg-green-100 text-green-600 hover:bg-green-200"
                      : "bg-purple-100 text-purple-600 hover:bg-purple-200"
                  }`}
                >
                  {copied ? "Copied!" : "Copy"}
                </button>
              </div>
              {expiresIn && (
                <div className="mt-2 text-sm text-gray-600 flex items-center">
                  <svg
                    className="w-4 h-4 mr-1"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  Link expires in {formatTimeRemaining(expiresIn)}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

import { useEffect, useState } from "react";

import { getAssetUrls, type AssetUrls } from "./api";

export default function App() {
  const [assets, setAssets] = useState<AssetUrls | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    getAssetUrls()
      .then((nextAssets) => {
        if (!cancelled) {
          setAssets(nextAssets);
        }
      })
      .catch((caught: unknown) => {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Unable to load assets");
        }
      })
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main>
      {assets ? (
        <video controls preload="metadata" src={assets.video_url}>
          Your browser does not support HTML video.
        </video>
      ) : error ? (
        <p role="alert">{error}</p>
      ) : (
        <p role="status">Loading video…</p>
      )}
    </main>
  );
}

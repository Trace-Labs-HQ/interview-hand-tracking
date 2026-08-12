export type AssetUrls = {
  video_url: string;
  hand_tracks_url: string;
  expires_in_seconds: number;
};

const API_BASE_URL = "http://localhost:8000";

export async function getAssetUrls(): Promise<AssetUrls> {
  const response = await fetch(`${API_BASE_URL}/api/assets`);
  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}`);
  }
  return response.json() as Promise<AssetUrls>;
}

import { afterEach, describe, expect, it, vi } from "vitest";

import { getAssetUrls } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("getAssetUrls", () => {
  it("requests the fixed backend endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          video_url: "https://example.com/video",
          hand_tracks_url: "https://example.com/tracks",
          expires_in_seconds: 900,
        }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await getAssetUrls();

    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/api/assets");
    expect(result.expires_in_seconds).toBe(900);
  });

  it("reports backend errors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500 }));

    await expect(getAssetUrls()).rejects.toThrow("Backend returned 500");
  });
});

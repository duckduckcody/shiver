import dotenv from "dotenv";
import { exec } from "child_process";
import { promisify } from "node:util";
import editly from "editly";

const promiseExec = promisify(exec);

dotenv.config();

const TWITCH_CLIENT_ID = process.env.TWITCH_CLIENT_ID;
const TWITCH_CLIENT_SECRET = process.env.TWITCH_CLIENT_SECRET;
const TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token";
const NMP_BROADCAST_ID = "21841789";
const TWITCH_SEARCH_URL = "https://api.twitch.tv/helix/videos";

const getTwitchToken = async () => {
  const res = await fetch(TWITCH_AUTH_URL, {
    method: "post",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      client_id: TWITCH_CLIENT_ID,
      client_secret: TWITCH_CLIENT_SECRET,
      grant_type: "client_credentials",
    }),
  });

  const json = await res.json();
  return json["access_token"];
};

const getLatestTwitchVods = async () => {
  const token = await getTwitchToken();
  const params = {
    user_id: NMP_BROADCAST_ID,
  };

  const url = new URL(TWITCH_SEARCH_URL);
  const serialisedParams = new URLSearchParams(params).toString();
  url.search = serialisedParams;

  const res = await fetch(url, {
    method: "get",
    headers: {
      "Client-Id": TWITCH_CLIENT_ID,
      Authorization: `Bearer ${token}`,
    },
  });
  const json = await res.json();
  return json;
};

const latestTwitchVods = await getLatestTwitchVods();

const latestTwitchVodId = latestTwitchVods["data"][0]["id"];

await promiseExec(
  `./TwitchDownloaderCLI clipdownload --id ${latestTwitchVodId} -o ./vods/clip.mp4`
);

await promiseExec(
  `./TwitchDownloaderCLI chatdownload --id ${latestTwitchVodId} -o ./chats/chat.json -E`
);

await promiseExec(
  `./TwitchDownloaderCLI chatrender -i ./chats/chat.json --output-args="-c:v libvpx-vp9 -crf 18 -b:v 2M -pix_fmt yuva420p ./chats/chat.webm" -o ./chats/chat.webm --background-color "#00000000"`
);

await editly({
  outPath: "./alpha.mp4",
  keepSourceAudio: true,
  clips: [
    {
      layers: [
        { type: "video", path: "./vods/clip.mp4" },
        {
          type: "video",
          path: "./chats/chat.webm",
          width: 0.15,
          height: 0.5,
          resizeMode: "contain",
          left: 0,
          top: 0,
        },
      ],
    },
  ],
});

import { AIStream, type AIStreamParser, type AIStreamCallbacks } from 'ai';

function parseUrlslabStream(): AIStreamParser {
  return data => {
    console.log("maybe data here")
    console.log(data)
    const text = data;

    return text;
  };
}

export function UrlslabStream(
  res: Response,
  cb?: AIStreamCallbacks,
): ReadableStream {
  return AIStream(res, parseUrlslabStream(), cb);
}

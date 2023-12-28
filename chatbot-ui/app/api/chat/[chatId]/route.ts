import {NextResponse} from 'next/server';
import {PassThrough} from 'stream';
import {sessionService} from "@/lib/urlslab-api/services/SessionService";
import {ChatCompletionRequest} from "@/lib/urlslab-api/models/Session";
import {StreamingTextResponse} from "ai";

// Set the runtime to edge for best performance
export const runtime = 'edge';

export async function POST(req: Request, {params}: { params: { chatId: string } }) {
  try {
    const request = await req.json()
    if (!request.messages) {
      return new Response('Missing messages', {
        status: 400
      });
    }
    const messages: string[] = request.messages.map((message: any) => {
      return message.content
    });

    const chatCompletion: ChatCompletionRequest = {human_input: messages[messages.length - 1]};
    const response = await sessionService.streamChatbotResponse(params.chatId, chatCompletion);

    const textEncoder = new TextDecoder();
    const reader = response.body.getReader();
    const readableStream = new ReadableStream({
      async pull(controller) {
        const {value, done} = await reader.read()

        if (done) {
          controller.close()
        } else {
          controller.enqueue(textEncoder.decode(value))
        }
      },
    });


    // Pipe the external API stream directly to the Next.js API response
    return new Response(readableStream, {
      headers: {
        'Content-Type': 'application/octet-stream',
      }
    })
  } catch (error) {
    console.error(error);
    return new Response('An error occurred while streaming the response', {
      status: 500
    });
  }
}

export async function DELETE(req: Request, {params}: { params: { chatId: string } }) {
  try {
    const response = await sessionService.deleteSession(params.chatId);
    return Response.json(response)
  } catch (error: any) {
    if (error.response) {
      const {status, data} = error.response;
      return Response.json(data, {status})
    } else {
      console.error(error);
      return Response.json('An error occurred while streaming the response', {
        status: 500
      });
    }
  }
}

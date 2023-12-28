import type { NextApiRequest, NextApiResponse } from 'next'
import {sessionService} from "@/lib/urlslab-api/services/SessionService";

// export default async function handler(req: NextApiRequest, res: NextApiResponse) {
//   if (req.method === 'POST') {
//     const { tenantId, chatId, sessionId } = req.query;
//
//     try{
//       const response = await sessionService.streamChatbotResponse(sessionId);
//
//       // Set headers to indicate a chunked response
//       res.setHeader('Content-Type', 'text/event-stream');
//       res.setHeader('Cache-Control', 'no-cache');
//       res.setHeader('Connection', 'keep-alive');
//
//       // Pipe the external API stream directly to the Next.js API response
//       response.data.pipe(res);
//     } catch (error) {
//       console.error(error);
//       res.status(500).send('An error occurred while streaming the response');
//     }
//   } else {
//     res.setHeader('Allow', ['POST']);
//     res.status(405).end(`Method ${req.method} Not Allowed`);
//   }
// };

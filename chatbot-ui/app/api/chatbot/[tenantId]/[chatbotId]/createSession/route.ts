import type {NextApiRequest, NextApiResponse} from 'next'
import {sessionService} from "@/lib/urlslab-api/services/SessionService";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    const {tenantId, chatbotId} = req.query;
    if (req.method === 'PUT') {
        await putHandler(Number.parseInt(tenantId as string), Number.parseInt(chatbotId as string), res)
    } else {
        res.setHeader('Allow', ['PUT']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
};

const putHandler = async (tenantId: number, chatbotId: number, res: NextApiResponse) => {
    try {
        const response = await sessionService.createSession(tenantId, chatbotId);
        res.status(201).json(response.data);
    } catch (error: any) {
        if (error.response) {
            const { status, data } = error.response;
            res.status(status).json(data);
        } else {
            console.error(error);
            res.status(500).send('An error occurred while creating the session');
        }
    }
}

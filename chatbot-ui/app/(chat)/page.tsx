import {nanoid} from '@/lib/utils'
import {Chat} from '@/components/chat'
import {sessionService} from "@/lib/urlslab-api/services/SessionService";
import {HTTPValidationError} from "@/lib/urlslab-api/models/HttpError";
import {SessionResponse} from "@/lib/urlslab-api/models/Session";
import ErrorHandler from "@/components/error-handler";

export default async function IndexPage() {

    // TODO - Get the recent tenant id and recent chatbot id from db
    // default to first entry response from tenants and chatbots
    try {
        const chatSession = await sessionService.createSession(1, 3)
        if ((chatSession as HTTPValidationError).detail !== undefined) {
            // Error in getting the session
            return (<section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
                <div className="flex max-w-[980px] flex-col items-start gap-2">
                    <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
                        No Chatbot. head to chatbots page to create one.
                    </h1>
                    <p className="max-w-[700px] text-lg text-muted-foreground">
                        Each chatbot is associated with its own AI model, and system prompt. all chatbots are connected
                        to the same knowledge base.
                    </p>
                </div>
            </section>)
        }
        return <Chat id={(chatSession as SessionResponse).session_id}/>
    } catch (e: any) {
        return <ErrorHandler error={e} />
    }


}

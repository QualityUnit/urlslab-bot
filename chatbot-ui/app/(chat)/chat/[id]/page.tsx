// @ts-nocheck

import { type Metadata } from 'next'
import { notFound, redirect } from 'next/navigation'

import { getChat } from '@/app/actions'
import { Chat } from '@/components/chat'
import {useSession} from "next-auth/react";

export interface ChatPageProps {
  params: {
    id: string
  }
}

// @ts-nocheck
export async function generateMetadata({
  params
}: ChatPageProps): Promise<Metadata> {
  const session = useSession()

  if (!session?.user) {
    return {}
  }

  const chat = await getChat(params.id, session.user.id)
  return {
    title: 'Chat'
  }
}

export default async function ChatPage({ params }: ChatPageProps) {
  const session = useSession()

  console.log("session", session)

  if (!session?.user) {
    redirect(`/sign-in?next=/chat/${params.id}`)
  }

  const chat = await getChat(params.id, session.user.id)

  if (!chat) {
    notFound()
  }

  // if (chat?.userId !== session?.user?.id) {
  //   notFound()
  // }

  return <Chat id="test" initialMessages={[]} />
}

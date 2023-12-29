'use client'

import { Sidebar } from '@/components/sidebar'

import { ChatHistory } from '@/components/chat-history'
import {useSession} from "next-auth/react";
import {getServerSession} from "next-auth";
import {authOptions} from "@/app/api/auth/[...nextauth]/route";

export function ChatbotSidebarDesktop() {
  const { data } = useSession()

  if (!data?.user?.id) {
    return null
  }

  return (
    <Sidebar className="peer absolute inset-y-0 right-0 z-30 hidden translate-x-full border-l bg-muted duration-300 ease-in-out data-[state=open]:translate-x-0 lg:flex lg:w-[400px] xl:w-[500px]">
      <p>Sample text here for now</p>
    </Sidebar>
  )
}

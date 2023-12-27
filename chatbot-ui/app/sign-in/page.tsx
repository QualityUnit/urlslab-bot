"use client";

import { redirect } from 'next/navigation'
import {LoginCard} from "@/components/login-card";
import {useSession} from "next-auth/react";

export default function SignInPage() {
  const { data } = useSession()

  // redirect to home if user is already logged in
  if (data?.user) {
    redirect('/')
  }

  return (
    <div className="flex h-[calc(100vh-theme(spacing.16))] items-center justify-center py-10">
      <LoginCard />
    </div>
  )
}

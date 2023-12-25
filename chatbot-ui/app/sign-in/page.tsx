import { auth } from '@/auth'
import { redirect } from 'next/navigation'
import {LoginCard} from "@/components/login-card";
import {signIn} from "next-auth/react";

export default async function SignInPage() {
  const session = await auth()
  // redirect to home if user is already logged in
  if (session?.user) {
    redirect('/')
  }

  const handleSubmit = async (email: string, password: string) => {
    // Call the signIn function from next-auth
    // The credentials type should match with the CredentialsProvider configuration
    const res = await signIn('credentials', {
      redirect: false,
      email,
      password,
    });

    if (res?.ok) {
      // Redirect to some page upon successful sign-in
      window.location.href = '/some-protected-page';
    } else {
      // Handle errors, e.g., show an error message.
      console.error('Sign-in failed: ', res.error);
    }
  };

  return (
    <div className="flex h-[calc(100vh-theme(spacing.16))] items-center justify-center py-10">
      <LoginCard onSubmit={handleSubmit} />
    </div>
  )
}

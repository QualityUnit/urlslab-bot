import NextAuth, {DefaultSession} from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { AuthService } from '@/lib/urlslab-api'
import { PrismaAdapter } from "@auth/prisma-adapter"
import { PrismaClient } from "@prisma/client"

declare module 'next-auth' {
  interface Session {
    user: {
      /** The user's id. */
      username: string
      email: string
    } & DefaultSession['user']
  }
}


const prisma = new PrismaClient()

export const {
  handlers: { GET, POST },
  auth
} = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
      username: { label: "Username", type: "text", placeholder: "username" },
      password: { label: "Password", type: "password" }
    },
      async authorize(credentials, request) {
        const authService = new AuthService();
        const tokenResponse = await authService.loginUser({
            email: credentials.email,
            password: credentials.password
        });

        // Assuming your `AuthService` returns a `tokenResponse` which includes a user `id`.
        if (tokenResponse && tokenResponse.user.username && tokenResponse.user.email) {
          // Return a user object with the required `id` property
          return { username: tokenResponse.user.username, email: tokenResponse.user.email };
        } else {
          // If authentication fails, return null
          return null;
        }
      },
    }),
  ],
  callbacks: {
    jwt: async ({ token, user }) => {
      if (user) {
        // Store only the user `id` in the token
        token.email = user.email;
      }
      return token;
    },
    session: async ({ session, token }) => {
      if (token.email) {
        // Store only the user `id` in the session
        session.user = { username: '', email: token.email };
      }
      return session;
    },
  },
  pages: {
    signIn: "/sign-in", // If you have a custom login page
  },
});
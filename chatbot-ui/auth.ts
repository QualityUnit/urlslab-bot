import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { AuthService } from '@/lib/urlslab-api'

declare module 'next-auth' {
  interface Session {
    user: {
      /** The user's id. */
      id: string
    } & DefaultSession['user']
  }
}

export const {
  handlers: { GET, POST },
  auth
} =  NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: {  label: "Password", type: "password" }
      },
      authorize: async (credentials) => {
        const authService = new AuthService();

        console.log(credentials)

        if (credentials) {
          // Use authService to authenticate the user
          const token = await authService.loginUser({
            email: credentials.email,
            password: credentials.password
          })

          if (token) {
            // Any user object returned here will be saved in the JWT
            // The user object should be returned with an `id` field
            return { id: 'user-id', email: credentials.email }
          }
        }
        // If you return null or false then the credentials will be rejected
        return null;
      }
    })
  ],
  callbacks: {
    session: async ({ session, user }) => {
      if (session.user) {
        session.user.id = user.id; // Assign the id from user object to the session
      }
      return session;
    },
  },
})
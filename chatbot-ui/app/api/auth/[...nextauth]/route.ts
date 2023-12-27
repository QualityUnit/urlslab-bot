import NextAuth from "next-auth";
import {userService} from "@/lib/services/UserService";
import CredentialsProvider from "next-auth/providers/credentials";

if (!process.env.NEXTAUTH_SECRET) {
  throw new Error("Please provide process.env.NEXTAUTH_SECRET");
}

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'creds',
      credentials: {
        email: { label: "Email", type: "text" },
        password: {  label: "Password", type: "password" }
      },
      async authorize(credentials, req) {
        // Here you look up the user in your database
        {/* @ts-ignore */}
        const { email, password } = credentials;

        if (!email || !password) {
            return null;
        }

        const user = await userService.signInCredentials(email, password);
        return user
      }
    }),
  ],
  debug: true,
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.email = user.email;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id;
        session.user.email = token.email;
        session.user.role = token.role;
      }
      return session;
    }
  },
  pages: {
    signIn: '/sign-in', // Specifies a custom signin page if needed
  },
});


export { handler as GET, handler as POST, handler as authOptions }
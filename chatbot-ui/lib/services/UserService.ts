import {IUser, Role} from 'nextauth'; // Assuming User is imported from Prisma
import bcrypt from 'bcryptjs';
import prisma from "@/lib/services/helpers/prisma_client";
import {IUserService} from "@/lib/services/IUserService";
import {User} from "next-auth";

export class PrismaUserService implements IUserService {
  salts: number;

  constructor() {
    this.salts = 10;
  }

  async signInCredentials(email: string, password: string): Promise<User> {
    // Continue with regular sign-in for non-admin users
    console.log("SIGN IN CREDENTIALS")

    const user = await prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (!user || !user.password || !bcrypt.compareSync(password, user.password)) {
      throw new Error('Invalid email or password');
    }

    // The password is correct, return the user (excluding the password)
    return {
        id: user.id,
        email: user.email,
        role: user.role as Role,
    };
  }
}

export const userService = new PrismaUserService();
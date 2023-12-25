import * as React from "react"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function LoginCard(onSubmit: (email: string, password: string) => Promise<void>) {
  const [email, setEmail] = React.useState("")
    const [password, setPassword] = React.useState("")

  return (
    <Card className="w-[600px]">
      <CardHeader>
        <CardTitle>Create and manage your own chatbot</CardTitle>
        <CardDescription>Deploy and manage your very own chatbot with your own custom documents and knowledge base. deploy with one click.</CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="email">Email</Label>
              <Input id="email" placeholder="Your Email"/>
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" placeholder="Your Password"/>
            </div>
          </div>
        </form>
          <p className="mt-5 text-sm text-muted-foreground">No account? contact admin of your organization.</p>
      </CardContent>
      <CardFooter className="flex justify-end">
        <Button onClick={() => onSubmit(email, password)}>Sign In</Button>
      </CardFooter>
    </Card>
  )
}

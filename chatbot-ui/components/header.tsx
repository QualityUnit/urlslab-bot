import * as React from 'react'
import Link from 'next/link'

import { auth } from '@/auth'
import { Button, buttonVariants } from '@/components/ui/button'
import { Icons } from "@/components/icons"
import {
  IconNextChat,
  IconSeparator,
} from '@/components/ui/icons'
import { ThemeToggle } from '@/components/theme-toggle'
import { UserMenu } from '@/components/user-menu'
import { SidebarMobile } from './sidebar-mobile'
import { SidebarToggle } from './sidebar-toggle'
import { ChatHistory } from './chat-history'
import {MainNav} from "@/components/main-nav";
import {siteConfig} from "@/config/site";

async function UserOrLogin() {
  const session = await auth()
  return (
    <>
      {session?.user ? (
        <>
          <SidebarMobile>
            <ChatHistory userId={session.user.id} />
          </SidebarMobile>
          <SidebarToggle />
        </>
      ) : (
        <Link href="/" target="_blank" rel="nofollow">
          <IconNextChat className="w-6 h-6 mr-2 dark:hidden" inverted />
          <IconNextChat className="hidden w-6 h-6 mr-2 dark:block" />
        </Link>
      )}
      <div className="flex items-center">
        <IconSeparator className="w-6 h-6 text-muted-foreground/50" />
        {session?.user ? (
          <UserMenu user={session.user} />
        ) : (
          <Button variant="link" asChild className="-ml-2">
            <Link href="/sign-in?callbackUrl=/">Login</Link>
          </Button>
        )}
      </div>
    </>
  )
}

export function Header() {
  return (
      <header className="bg-background sticky top-0 z-40 w-full border-b">
        <div className="container flex h-16 items-center space-x-4 sm:justify-between sm:space-x-0">
          <MainNav items={siteConfig.mainNav}/>
          <div className="flex flex-1 items-center justify-end space-x-4">
            <nav className="flex items-center space-x-1">
              <Link
                  href={siteConfig.links.github}
                  target="_blank"
                  rel="noreferrer"
              >
                <div
                    className={buttonVariants({
                      size: "icon",
                      variant: "ghost",
                    })}
                >
                  <Icons.gitHub className="h-5 w-5"/>
                  <span className="sr-only">GitHub</span>
                </div>
              </Link>
              <Link
                  href={siteConfig.links.twitter}
                  target="_blank"
                  rel="noreferrer"
              >
                <div
                    className={buttonVariants({
                      size: "icon",
                      variant: "ghost",
                    })}
                >
                  <Icons.twitter className="h-5 w-5 fill-current"/>
                  <span className="sr-only">Twitter</span>
                </div>
              </Link>
              <ThemeToggle/>
            </nav>
          </div>
        </div>
      </header>
  )
}

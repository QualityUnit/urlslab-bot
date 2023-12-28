
export default function ErrorHandler(error: any) {
    return (<section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
            <div className="flex max-w-[980px] flex-col items-start gap-2">
                <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
                    Oops Something went wrong!
                </h1>
                <p className="max-w-[700px] text-lg text-muted-foreground">
                    Make sure chatbot ui can communicate properly to urlslab bot api.
                    {error.error.detail && (<span>here is more detail about the error:
                        <br/>
                        <code>
                            {error.error.detail}
                        </code></span>)}
                </p>
            </div>
        </section>)
}

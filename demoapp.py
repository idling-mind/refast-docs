from fastapi import FastAPI, HTTPException
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, Text
from refast.security import RateLimiter

app = FastAPI()

# 1. Initialize rate limiter (Max 5 requests per 30 seconds)
limiter = RateLimiter(max_requests=5, window_seconds=30)

ui = RefastApp(title="Rate Limited Refast App")

@ui.page("/")
async def home(ctx: Context):
    # During page functions, ctx._request is populated with the Starlette Request
    print(ctx.request)
    if ctx.request:
        allowed, info = await limiter.is_allowed(ctx.request)
        print(allowed, info)
        if not allowed:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. Try again in {info['reset']} seconds."
            )
            
    return Column(
        class_name="p-8 h-screen",
        align="center",
        justify="center",
        children=[
            Heading("Rate Limited Page"),
            Text("Welcome! If you reload this page too many times, you will be rate-limited.")
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
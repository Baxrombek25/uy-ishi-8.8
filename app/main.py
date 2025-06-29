from fastapi import FastAPI
from app.database import Base, engine
from app.auth import auth_routes
from app.routes import user_routes,review_routes,admin_routes, category_routes, product_routes, cart_routes, order_routes
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


app = FastAPI(title="ShopTime API")

app.include_router(auth_routes.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(product_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)
app.include_router(admin_routes.router)
app.include_router(review_routes.router)

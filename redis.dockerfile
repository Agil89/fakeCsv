FROM redis:4.0.11

ENV REDIS_PASSWORD test123

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]




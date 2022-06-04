FROM node:18

WORKDIR /app
COPY ../app/package* ./
RUN npm install

COPY ../app ./
CMD npm run dev

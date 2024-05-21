# этап сборки (build stage)
FROM node:lts-alpine
WORKDIR /app

# создаем слой пакетов, чтобы не переустанавливать в каждом релизе
COPY package*.json ./
RUN npm install
RUN npm install -g @quasar/cli
RUN npm install -g @vue/cli-service@latest
COPY . .
EXPOSE 9000
CMD ["npm", "run", "dev"]

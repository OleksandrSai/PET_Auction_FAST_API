FROM node:20-bullseye

WORKDIR /frontend

COPY ../../frontend/package*.json ./

RUN npm install

COPY ../../frontend/ .

EXPOSE 4200

CMD ["npm", "run", "start"]

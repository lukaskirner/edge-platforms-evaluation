FROM node:16.4.2 as builder

COPY . .
RUN yarn install
RUN yarn build


####################################################
FROM nginx:1.20.1-alpine

COPY --from=builder ./build /usr/share/nginx/html

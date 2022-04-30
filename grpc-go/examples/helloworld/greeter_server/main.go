/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

// Package main implements a server for Greeter service.
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"
	"github.com/garyburd/redigo/redis"
	pb "google.golang.org/grpc/examples/helloworld/helloworld"
)

var (
	port = flag.Int("port", 50051, "The server port")
)

// server is used to implement helloworld.GreeterServer.
type server struct {
	pb.UnimplementedGreeterServer
}

// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
    a := in.GetPointX()
    b := in.GetPointY()
    index_x := a / 72
    index_y := b / 128
    index := index_y * 10 + index_x
    log.Printf("Index = %v", index)

    conn, err := redis.Dial("tcp", "127.0.0.1:6379")
    if err != nil {
		fmt.Println("redis.Dial err=", err)
	}
    img_name := "sub_img_" + fmt.Sprint(index)
    r, err := redis.String(conn.Do("Get", img_name))
    if err != nil {
		fmt.Println("set err=", err)
	}
	// fmt.Println("Manipulate success, the name is", r)

	log.Printf("Received point: %v, %v", in.GetPointX(), in.GetPointY())

	return &pb.HelloReply{Index:index, Message: r}, nil
}


func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

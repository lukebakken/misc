package io.bakken.basic_publish;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.AMQP.Queue.DeclareOk;

public class App 
{
    public static void main(String[] argv) throws Exception {
        final ConnectionFactory factory = new ConnectionFactory();
        factory.setRequestedHeartbeat(5);
        factory.setHost(System.getenv("RMQ_HOST"));
		factory.setUsername("guest");
        factory.setPassword("guest");
        factory.setVirtualHost("/");
        final Connection connection = factory.newConnection();
        final Channel channel = connection.createChannel();

        DeclareOk q = channel.queueDeclare();
        System.out.printf("[INFO] publishing messages to %s, start toxic at any point", q.getQueue());

        int i = 0;
        byte[] body = "HELLO WORLD".getBytes();
        while (true) {
            System.out.printf("[INFO] publishing message %d%n", i);
            channel.basicPublish("", q.getQueue(), null, body);
            i++;
            Thread.sleep(1000);
        }
    }
}

package io.bakken.basic_publish;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.AMQP.Queue.DeclareOk;
import java.time.ZonedDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;

public class App 
{
    public static String now()
    {
        return ZonedDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.ISO_INSTANT);
    }

    public static void main(String[] argv) throws Exception {
        final byte[] body = "HELLO WORLD".getBytes();
        final ConnectionFactory factory = new ConnectionFactory();
        factory.setRequestedHeartbeat(5);
        factory.setHost(System.getenv("RMQ_HOST"));
        factory.setPort(55672);
		factory.setUsername("guest");
        factory.setPassword("guest");
        factory.setVirtualHost("/");
        final Connection connection = factory.newConnection();
        final Channel channel = connection.createChannel();
        channel.confirmSelect();

        channel.addConfirmListener(
            (deliveryTag, multiple) ->
                System.out.printf("[INFO] %s confirmed: %d%n", now(), deliveryTag),
            (deliveryTag, multiple) ->
                System.out.printf("[INFO] %s nacked: %d%n", now(), deliveryTag)
        );

        DeclareOk q = channel.queueDeclare();
        System.out.printf("[INFO] %s publishing messages to %s, start toxic at any point",
                now(), q.getQueue());

        int i = 0;
        while (true) {
            System.out.printf("[INFO] %s publishing message %d%n", now(), i);
            channel.basicPublish("", q.getQueue(), null, body);
            i++;
            Thread.sleep(1000);
        }
    }
}

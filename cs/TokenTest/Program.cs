// See https://aka.ms/new-console-template for more information
using System.Net;
using System.Net.Sockets;
using System.Text;

async Task<TcpClient> Connect(TimeSpan timeout, CancellationToken cancellationToken)
{
    using var timeoutTokenSource = new CancellationTokenSource(timeout);
    using var lts = CancellationTokenSource.CreateLinkedTokenSource(timeoutTokenSource.Token, cancellationToken);

    IPAddress[] ips = await Dns.GetHostAddressesAsync("127.0.0.1", lts.Token);
    IPAddress addr = ips.First();
    var ep = new IPEndPoint(addr, 12345);
    Console.WriteLine("[INFO] connecting to: {0}", ep);

    var client = new TcpClient();
    try
    {
        await client.ConnectAsync(ep, lts.Token);
    }
    catch (OperationCanceledException opex)
    {
        if (opex.CancellationToken == timeoutTokenSource.Token)
        {
            Console.Error.WriteLine("[ERROR] timeout connecting to ep: {0}, ex: {1}", ep, opex);
        }
        else
        {
            Console.Error.WriteLine("[ERROR] operation canceled connecting to ep: {0}, ex: {1}", ep, opex);
        }
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine("[ERROR] exception connecting to ep: {0}, ex: {1}", ep, ex);
    }

    return client;
}

async Task Get(TcpClient client, TimeSpan timeout, CancellationToken cancellationToken)
{
    using var timeoutTokenSource = new CancellationTokenSource(timeout);
    using var lts = CancellationTokenSource.CreateLinkedTokenSource(timeoutTokenSource.Token, cancellationToken);

    // NOTE: this is only for synchronous send/receive
    client.SendTimeout = (int)timeout.TotalMilliseconds;
    client.ReceiveTimeout = (int)timeout.TotalMilliseconds;

    byte[] buffer = new byte[1024];
    byte[] request = Encoding.UTF8.GetBytes("HELLO\n");

    try
    {
        NetworkStream ns = client.GetStream();
        await ns.WriteAsync(request, lts.Token);
        int bytesRead = await ns.ReadAsync(buffer, lts.Token);

        Console.WriteLine("[INFO] read {0} bytes, response is: {1}", bytesRead, Encoding.UTF8.GetString(buffer, 0, bytesRead));
    }
    catch (OperationCanceledException opex)
    {
        if (opex.CancellationToken == timeoutTokenSource.Token)
        {
            Console.Error.WriteLine("[ERROR] 0 timeout writing/reading, ex: {0}", opex);
        }
        else if (opex.CancellationToken == cancellationToken)
        {
            Console.Error.WriteLine("[ERROR] 1 operation canceled writing/reading, ex: {0}, inner: {1}",
                opex, opex.InnerException);
        }
        else if (opex.CancellationToken == lts.Token)
        {
            if (timeoutTokenSource.Token.IsCancellationRequested)
            {
                Console.Error.WriteLine("[ERROR] 2.0 timeout writing/reading, ex: {0}", opex);
            }
            else if (cancellationToken.IsCancellationRequested)
            {
                Console.Error.WriteLine("[ERROR] 2.1 operation canceled writing/reading, ex: {0}, inner: {1}",
                    opex, opex.InnerException);
            }
        }
        else
        {
            Console.Error.WriteLine("[ERROR] 3 operation canceled writing/reading, ex: {0}, inner: {1}",
                opex, opex.InnerException);
        }
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine("[ERROR] exception writing/reading, ex: {0}", ex);
    }
}

// var timeout = TimeSpan.FromMilliseconds(250);
var timeout = TimeSpan.FromSeconds(1);
using var cts = new CancellationTokenSource();
cts.CancelAfter(750);
TcpClient client = await Connect(timeout, cts.Token);
await Get(client, timeout, cts.Token);

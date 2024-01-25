WorkerWithTimer? worker = null;
var cts = new CancellationTokenSource();
try
{
    // Task for UI thread, so we can call Task.Wait wait on the main thread.
    _ = Task.Run(() =>
    {
        Console.WriteLine("Press 'c' to cancel within 3 seconds after work begins.");
        Console.WriteLine("Or let the task time out by doing nothing.");
        if (Console.ReadKey(true).KeyChar == 'c')
        {
            cts.Cancel();
        }
    });

    // Let the user read the UI message.
    await Task.Delay(1000);

    // Start the worker task.
    worker = new WorkerWithTimer(cts.Token);
    Task task = Task.Run(worker.DoWork, cts.Token);

    try
    {
        await task.WaitAsync(cts.Token);
    }
    catch (OperationCanceledException e)
    {
        if (e.CancellationToken == cts.Token)
        {
            Console.WriteLine("Main: canceled from UI thread throwing OCE.");
        }
    }
    catch (AggregateException ae)
    {
        Console.WriteLine("AggregateException caught: " + ae.InnerException);
        foreach (var inner in ae.InnerExceptions)
        {
            Console.WriteLine(inner.Message + inner.Source);
        }
    }
    Console.WriteLine("Press any key to exit.");
    Console.ReadKey();
}
finally
{
    worker?.Dispose();
    cts.Dispose();
}

class WorkerWithTimer : IDisposable
{
    // private readonly CancellationTokenSource internalTokenSource = new();
    private readonly CancellationTokenSource internalTokenSource;
    private readonly CancellationToken externalToken;
    private readonly CancellationToken internalToken;
    // private readonly Timer timer;

    public WorkerWithTimer(CancellationToken externalToken)
    {
        this.internalTokenSource = new CancellationTokenSource(TimeSpan.FromSeconds(3));
        this.internalToken = internalTokenSource.Token;
        this.externalToken = externalToken;

        // A toy cancellation trigger that times out after 3 seconds
        // if the user does not press 'c'.
        // this.timer = new Timer(new TimerCallback(CancelAfterTimeout), null, 3000, 3000);
    }

    //<snippet7>
    public void DoWork()
    {
        // Create a new token that combines the internal and external tokens.
        using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(internalToken, externalToken);
        try
        {
            DoWorkInternal(linkedCts.Token);
        }
        catch (OperationCanceledException)
        {
            if (internalToken.IsCancellationRequested)
            {
                Console.WriteLine("DoWork: operation timed out (internalToken)");
            }
            else if (externalToken.IsCancellationRequested)
            {
                Console.WriteLine("DoWork: cancelling per user request (externalToken)");
                externalToken.ThrowIfCancellationRequested();
            }
        }
    }

    private void DoWorkInternal(CancellationToken token)
    {
        for (int i = 0; i < 1000; i++)
        {
            if (token.IsCancellationRequested)
            {
                Console.WriteLine("DoWorkInternal: cancelling per user request.");

                // We need to dispose the timer if cancellation
                // was requested by the external token.
                // timer.Dispose();

                // Throw the exception.
                token.ThrowIfCancellationRequested();
            }

            // Simulating work.
            Thread.SpinWait(10000000);
            Console.Write("working...{0}", Environment.NewLine);
        }
    }

    /*
    public void CancelAfterTimeout(object? state)
    {
        Console.WriteLine("\r\nTimer fired.");
        internalTokenSource.Cancel();
        timer.Dispose();
    }
    */

    public void Dispose()
    {
        internalTokenSource.Dispose();
        // timer.Dispose();
    }
}

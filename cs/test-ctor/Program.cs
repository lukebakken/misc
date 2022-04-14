namespace TestCtor
{
    public class Klass
    {
        private readonly object _thing = new object();

        public Klass()
        {
            Console.WriteLine("0 _thing: {0}", _thing.GetHashCode());
        }

        public Klass(object thing) : this()
        {
            Console.WriteLine("1 thing arg: {0}", thing.GetHashCode());
            _thing = thing;
            Console.WriteLine("1 _thing: {0}", _thing.GetHashCode());
        }

        public object Thing
        {
            get { return _thing; }
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("START 0-arg ctor");
            var k0 = new Klass();
            Console.WriteLine("k0.Thing: {0}", k0.Thing.GetHashCode());
            Console.WriteLine("END 0-arg ctor");
            Console.WriteLine();

            Console.WriteLine("START 1-arg ctor");
            var my_thing = new object();
            Console.WriteLine("my_thing: {0}", my_thing.GetHashCode());
            var k1 = new Klass(my_thing);
            Console.WriteLine("k1.Thing: {0}", k1.Thing.GetHashCode());
            Console.WriteLine("END 1-arg ctor");
        }
    }
}

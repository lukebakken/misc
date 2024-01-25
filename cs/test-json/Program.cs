// See https://aka.ms/new-console-template for more information
using System.Text.RegularExpressions;

// Regex rex = new Regex(@"^(?<pid><[^>]*>)\s\[.*""connection_name"",""(?<connection_name>[^""]*)"".*\]$", RegexOptions.Multiline | RegexOptions.Compiled);
Regex rex = new Regex(@"^\[.*""connection_name"",""(?<connection_name>[^""]*)"".*\]$", RegexOptions.Multiline | RegexOptions.Compiled);

const string s = "[{\"product\",\"RabbitMQ\"},{\"version\",\"7.0.0-alpha.2.24+abf8086f6e6ca5fefec8bed500ac28fa0647db60\"},{\"platform\",\".NET\"},{\"copyright\",\"Copyright (c) 2007-2020 VMware, Inc.\"},{\"information\",\"Licensed under the MPL. See https://www.rabbitmq.com/\"},{\"capabilities\",[{\"publisher_confirms\",true},{\"exchange_exchange_bindings\",true},{\"basic.nack\",true},{\"consumer_cancel_notify\",true},{\"connection.blocked\",true},{\"authentication_failure_close\",true}]},{\"connection_name\",\"SI.TestConnectionRecovery.TestBasicChannelRecovery:2024-01-16T20:23:54.6576534Z:1\"}]\r\n";
string s1 = s.Trim();

Match m = rex.Match(s1);

Console.WriteLine("@@@@@@@@ match: {0}", m);

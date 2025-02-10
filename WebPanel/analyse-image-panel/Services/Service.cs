using System.Text.Json;
using analyse_image_panel.Dtos;
using analyse_image_panel.WebClients;

namespace analyse_image_panel.Services
{
    public class Service : IService
    {
        protected string UrlApi;
        protected IWebClient webClient;

        public Service(HttpClient client)
        {
            UrlApi = "http://149.7.5.30:21090";
            client.BaseAddress = new Uri(UrlApi);
            webClient = new WebClient(client);
        }

        public async Task<PlaqueDTO?> RecupererContenuPlaqueAsync(byte[] Image)
        {
            return await webClient.RecupererContenuPlaqueAsync(Image);
        }
    }
}
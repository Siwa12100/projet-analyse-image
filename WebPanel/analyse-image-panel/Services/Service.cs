using System.Text.Json;
using analyse_image_panel.Dtos;

namespace analyse_image_panel.Services
{
    public class Service : IService
    {
        protected string UrlApi;
        protected HttpClient Client;

        public Service(HttpClient client)
        {
            UrlApi = "http://149.7.5.30:2190";
            this.Client = client;
        }

        public async Task<PlaqueDTO?> RecupererContenuPlaqueAsync(byte[] Image)
        {
            string routeApi = "/api/detection";
            var content = new MultipartFormDataContent();
            content.Add(new ByteArrayContent(Image), "file", "file.jpg");

            var response = await Client.PostAsync(UrlApi + routeApi, content);

            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            var responseContent = await response.Content.ReadFromJsonAsync<PlaqueDTO>();
            return responseContent;       
        }
    }
}
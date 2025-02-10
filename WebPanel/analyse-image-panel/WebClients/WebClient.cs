using System.Net.Http.Headers;
using System.Net.Http.Json;
using analyse_image_panel.Dtos;

namespace analyse_image_panel.WebClients
{
    public class WebClient : IWebClient
    {
        private readonly HttpClient _client;

        public WebClient(HttpClient client)
        {
            _client = client;
            _client.BaseAddress ??= new Uri("http://149.7.5.30:21090/");
        }

        public async Task<PlaqueDTO?> RecupererContenuPlaqueAsync(byte[] image)
        {
            using var content = new MultipartFormDataContent();
            using var imageContent = new ByteArrayContent(image);
            imageContent.Headers.ContentType = MediaTypeHeaderValue.Parse("image/jpeg");
            content.Add(imageContent, "file", "file.jpg");

            var response = await _client.PostAsync("detect", content); 

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine($"❌ Erreur lors de la classification ({response.StatusCode} - {response.ReasonPhrase})");
                Console.WriteLine(await response.Content.ReadAsStringAsync());
                return null;
            }

            try
            {
                var responseContent = await response.Content.ReadFromJsonAsync<PlaqueDTO>();
                return responseContent;
            }
            catch (Exception ex)
            {
                Console.WriteLine("⚠️ Erreur lors de la désérialisation de la réponse : " + ex.Message);
                return null;
            }
        }
    }
}

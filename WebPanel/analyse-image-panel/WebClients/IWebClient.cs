using analyse_image_panel.Dtos;

namespace analyse_image_panel.WebClients
{
    public interface IWebClient
    {
        Task<PlaqueDTO?> RecupererContenuPlaqueAsync(byte[] Image);
    }
}
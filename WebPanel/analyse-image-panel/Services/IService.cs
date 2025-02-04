using analyse_image_panel.Dtos;

namespace analyse_image_panel.Services
{
    public interface IService
    {
        Task<PlaqueDTO?> RecupererContenuPlaqueAsync(byte[] Image);
    }
}
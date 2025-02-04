using analyse_image_panel.Services;
using Microsoft.AspNetCore.Components;

namespace analyse_image_panel.Pages.Index
{
    public partial class Index
    {
        [Inject]
        protected IService? PlaqueService { get; set; }
    }
}
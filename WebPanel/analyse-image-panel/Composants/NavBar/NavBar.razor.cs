using Microsoft.AspNetCore.Components;

namespace projet_analyse_image.Composants.NavBar
{
    public partial class NavBar
    {
        [Inject]
        protected NavigationManager? NavigationManager { get; set; }

        private void RedirigerVersAccueil()
        {
            NavigationManager?.NavigateTo("/");
        }
    }
}
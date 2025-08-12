using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Ml_Sales_Profit.Models;

namespace Ml_Sales_Profit.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult upload()
        {
            return View();
        }

        public IActionResult roles()
        {
            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        public IActionResult users()
        {
            return View();
        }

        public IActionResult predict()
        {
            return View();
        }


        public IActionResult home()
        {
            return View();
        }

        public IActionResult login()
        {
            return View();
        }

        public IActionResult Allpredict()
        {
            return View();
        }

        public IActionResult predictbyuser()
        {
            return View();
        }



        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}

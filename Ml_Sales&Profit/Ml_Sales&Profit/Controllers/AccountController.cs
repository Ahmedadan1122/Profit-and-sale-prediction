using Microsoft.AspNetCore.Mvc;

public class AccountController : Controller
{
    [HttpPost]
    public IActionResult SetSession([FromBody] SessionModel model)
    {
        HttpContext.Session.SetString("userRole", model.Role);
        HttpContext.Session.SetString("userId", model.Id.ToString());
        HttpContext.Session.SetString("name", model.name);
        HttpContext.Session.SetString("email", model.email);
        return Ok();
    }

    [HttpGet]
    public IActionResult GetSession()
    {
        var role = HttpContext.Session.GetString("userRole");
        var id = HttpContext.Session.GetString("userId");
        var name = HttpContext.Session.GetString("name");
        var email = HttpContext.Session.GetString("email");

        return Json(new { role, id , name, email });
    }

    [HttpPost]
    public IActionResult Logout()
    {
        HttpContext.Session.Clear();
        return RedirectToAction("Login", "Home");
    }
}

public class SessionModel
{
    public string Role { get; set; }
    public string name { get; set; }
    public string email { get; set; }
    public int Id { get; set; }
}

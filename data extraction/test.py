raw = """
<h3>„mini top!”</h3>
				<a class="fancy" href="/image/shops/263b/mini-top.jpg"><img src="/image/shops/263b/mini-top.jpg"></a>
				<p>&nbsp;</p>
				<p style="text-align:center;">Viļakas 24A, Žīguri, Žīguru pagasts, Viļakas novads</p>
				<p>Darba laiks</p>
<p>P.-Pk. 8:00- 18:00</p>
<p>Se. 8:00-16:00</p>
<p>Sv. 8:00-16:00</p>
<p><a href="mailto:minitop.ziguri@madara89.lv">minitop.ziguri@madara89.lv</a></p>
<p>&nbsp;</p>
				<p><a href="tel:25713789">Tel nr. 25713789</a></p>
				<p>
					<a target="_blank" href="http://maps.google.com/maps?q=57.265518,27.666883&ll=57.265518,27.666883&z=17">Google map links</a><br>
				</p>
				<a class="closer" href="">Aizvērt ❯</a>


"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(raw, 'html.parser')

print(soup.find_all('p'))

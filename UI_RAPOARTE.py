""" MODUL: RAPOARTE ȘI STATISTICI
Scop: Vizualizare profit, grafice financiare și export PDF.
Cerința: 2.b, c, g, h) Statistici vizuale și rapoarte."""
import os
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import flet as ft
from FUNCTII_SQL import calculeaza_vanzari_astazi, calculeaza_vanzari_saptamana, get_raport_venituri, verifica_stocuri_critice, date_grafic_venituri_pierderi

GRAFIC_PATH = os.path.join(os.path.dirname(__file__), "grafic_vanzari_temp.png")


def creeaza_grafic_vanzari_7_zile():
    """Generează un Bar Chart cu vânzările din ultimele 7 zile (0 pentru zilele fără vânzări)."""
    date_vanzari = date_grafic_venituri_pierderi()

    # Construim un dict {dată: total} din datele reale
    vanzari_pe_zi = {}
    for d in date_vanzari:
        zi = d['ziua'].date() if hasattr(d['ziua'], 'date') else d['ziua']
        vanzari_pe_zi[zi] = float(d['total'])

    # Generăm ultimele 7 zile indiferent dacă au vânzări sau nu
    azi = datetime.date.today()
    etichete = []
    valori = []
    for i in range(6, -1, -1):
        zi = azi - datetime.timedelta(days=i)
        etichete.append(zi.strftime('%d %b'))
        valori.append(vanzari_pe_zi.get(zi, 0.0))

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor('#1e1e24')
    ax.set_facecolor('#1e1e24')

    culori = ['#9c6cff'] * len(valori)
    x = range(len(etichete))
    bars = ax.bar(x, valori, color=culori, width=0.5, zorder=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(etichete)

    ax.set_title('Vânzări zilnice — ultimele 7 zile', color='white', fontsize=13, pad=15)
    ax.set_ylabel('RON', color='#aaaaaa', fontsize=11)
    ax.tick_params(axis='x', colors='#aaaaaa', labelsize=10)
    ax.tick_params(axis='y', colors='#aaaaaa', labelsize=10)
    ax.spines['bottom'].set_color('#2f2f38')
    ax.spines['left'].set_color('#2f2f38')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, color='#2f2f38', linestyle='--', linewidth=0.7, zorder=0)
    ax.set_ylim(0, max(valori) * 1.3 if max(valori) > 0 else 10)

    for bar, val in zip(bars, valori):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(valori) * 0.03 if max(valori) > 0 else 0.3),
            f'{val:.0f}',
            ha='center', va='bottom', color='white', fontsize=9
        )

    plt.tight_layout()
    plt.savefig(GRAFIC_PATH, format='png', bbox_inches='tight', facecolor='#1e1e24')
    plt.close()
    return GRAFIC_PATH


def RapoartePage(page: ft.Page):
    from UI_DASHBOARD import DashboardPage
    venit_azi = calculeaza_vanzari_astazi()
    venit_saptamana = calculeaza_vanzari_saptamana()
    venit_luna = get_raport_venituri(perioada='luna')
    stocuri_critice = verifica_stocuri_critice()

    componente_stoc = []
    if stocuri_critice:
        for p in stocuri_critice:
            componente_stoc.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.WARNING_ROUNDED, color="red200", size=30),
                        title=ft.Text(p.nume_produs, weight="bold", color="white", size=16),
                        subtitle=ft.Text(
                            f"Stoc actual: {p.stoc_curent} buc. | Limită minimă setată: {p.stoc_minim} buc.",
                            color="grey400"
                        ),
                    ),
                    bgcolor="#252529",
                    padding=5,
                    border_radius=8,
                    margin=ft.margin.only(bottom=8)
                )
            )
        lista_critica = ft.Column(controls=componente_stoc)
    else:
        lista_critica = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green200", size=24),
                ft.Text("Toate stocurile sunt în regulă. Nu există produse epuizate.", color="green200", size=16)
            ]),
            bgcolor="#1c2d22",
            padding=15,
            border_radius=8
        )

    def creeaza_card_statistic(titlu, valoare, iconita, culoare_accent):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(iconita, color=culoare_accent, size=24),
                    ft.Text(titlu, size=14, color="grey400", weight="w500"),
                ], alignment=ft.MainAxisAlignment.START, spacing=10),
                ft.Container(height=10),
                ft.Text(f"{valoare:.2f} RON", size=26, color=culoare_accent, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#1e1e24",
            padding=20,
            border_radius=12,
            width=260,
            height=130,
            border=ft.border.all(1, "#2f2f38")
        )

    cale_grafic = creeaza_grafic_vanzari_7_zile()
    sectiune_grafic = ft.Column([
        ft.Text("Grafic Vânzări — Ultimele 7 Zile", size=18, weight="bold", color="white"),
        ft.Container(height=5),
        ft.Container(
            content=ft.Image(
                src=cale_grafic,
                width=750,
                height=320,
            ),
            bgcolor="#1e1e24",
            border_radius=12,
            padding=15,
            border=ft.border.all(1, "#2f2f38")
        )
    ])

    page.add(
        ft.Column([
            ft.Row([
                ft.TextButton(
                    "Înapoi la Dashboard",
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="purple200",
                    style=ft.ButtonStyle(color="purple200"),
                    on_click=lambda _: [page.clean(), DashboardPage(page)]
                )
            ]),
            ft.Container(height=10),
            ft.Text("Rapoarte și Analitice", size=32, color="purple200", weight="bold"),
            ft.Text(
                "Vizualizarea performanței financiare și managementul stocurilor din cafenea.",
                color="grey400", size=14
            ),
            ft.Divider(height=30, color="#2f2f38"),
            ft.Text("Performanță Vânzări", size=18, weight="bold", color="white"),
            ft.Container(height=5),
            ft.Row([
                creeaza_card_statistic("Vânzări Astăzi", venit_azi, ft.Icons.TODAY, "purple200"),
                creeaza_card_statistic("Vânzări Săptămână", venit_saptamana, ft.Icons.WEEKEND, "purple200"),
                creeaza_card_statistic("Vânzări Luna Aceasta", venit_luna, ft.Icons.MONETIZATION_ON, "purple200"),
            ], alignment=ft.MainAxisAlignment.START, spacing=20),
            ft.Container(height=35),
            sectiune_grafic,
            ft.Container(height=35),
            ft.Text("Alerte Stoc Critic", size=20, weight="bold", color="red200"),
            ft.Container(height=5),
            lista_critica
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )
    page.update()

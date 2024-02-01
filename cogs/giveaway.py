import disnake
from disnake.ext import commands
import asyncio
from disnake.ui import Button, View
import random

give_away_pool_user = []


class GiveAway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="giveaway",
        description="Создает эмбед с розыгрышем"
    )
    @commands.has_any_role(1022510823404478556, 1035268469387706498)  # YOURS ROLES ID
    async def giveaway(self, ctx, prize: str = commands.Param(description="Укажите приз"),
                       time: int = commands.Param(description="Укажите время (идет в минутах)")):

        give_away_pool = []
        time_in_seconds = time * 60
        avatar_url = ctx.author.display_avatar.url

        class ButtonConfirm(Button):
            def __init__(self, member):
                super().__init__(
                    style=disnake.ButtonStyle.green,
                    label="Участвовать",
                    custom_id="confirm",
                    emoji="✅"
                )
                self.member = member

            async def callback(self, interaction):
                if interaction.component.custom_id == "confirm":
                    if interaction.user.id not in give_away_pool:
                        give_away_pool.append(interaction.user.id)
                        await interaction.response.send_message(f"Вы присоединились к розыгрышу", ephemeral=True)
                    else:
                        await interaction.response.send_message("Вы уже зарегистрированы в розыгрыше", ephemeral=True)

        class ButtonCancel(Button):
            def __init__(self, member):
                super().__init__(
                    style=disnake.ButtonStyle.red,
                    label="Отменить участие",
                    custom_id="cancel",
                    emoji="❌"
                )
                self.member = member

            async def callback(self, interaction):
                if interaction.component.custom_id == "cancel":
                    if interaction.user.id in give_away_pool:
                        give_away_pool.remove(interaction.user.id)
                        await interaction.response.send_message("Вы успешно покинули розыгрыш", ephemeral=True)
                    else:
                        await interaction.response.send_message("Вы и так не участвуете в розыгрыше", ephemeral=True)

        class ButtonRerrol(Button):
            def __init__(self, member):
                super().__init__(
                    style=disnake.ButtonStyle.gray,
                    label="Реролл",
                    custom_id="reroll"
                )
                self.member = member

            async def callback(self, interaction):
                if interaction.component.custom_id == "reroll" and interaction.user.id == ctx.author.id:
                    if len(give_away_pool) > 0:
                        selected_winner = random.choice(give_away_pool)
                        await interaction.response.send_message(f"Новый победитель выбран: <@{selected_winner}>",
                                                                delete_after=3)
                        embed_winner = disnake.Embed(title="Победитель Розыгрыша",
                                                     description=f"Пользователь <@{selected_winner}> выиграл в розыгрыше\nОн получает **{prize}**\n",
                                                     color=disnake.Color.dark_theme())
                        embed_winner.set_thumbnail(url=selected_winner_user.display_avatar.url)
                        embed_winner.set_footer(text="Нажмите ниже для реролла или выдачи награды")
                        await interaction.message.edit(embed=embed_winner)
                    else:
                        await interaction.response.send_message(f"Нет участников, чтобы выполнить реролл",
                                                                ephemeral=True)

        class ButtonAccept(Button):
            def __init__(self, member):
                super().__init__(
                    style=disnake.ButtonStyle.gray,
                    label="Успешно",
                    custom_id="accept"
                )
                self.member = member

            async def callback(self, interaction):
                if interaction.component.custom_id == "accept" and interaction.user.id == ctx.author.id:
                    await interaction.response.send_message(f"Успешный розыгрыш", delete_after=3)
                    await asyncio.sleep(3)
                    await interaction.message.delete()
                    embed_for_user = disnake.Embed(title="Поздравляем вас с выигрышем",
                                                   description=f"Вы получили **{prize}**\nЖдем вас в новых розыгрышах")
                    embed_winner.set_thumbnail(url=selected_winner_user.display_avatar.url)
                    user = selected_winner_user
                    if user:
                        await user.send(embed=embed_for_user)

        embed = disnake.Embed(title="Розыгрыш",
                              description=f"**{prize}**\nВремя : **{time}м.**\nДля участия нажмите кнопку ниже",
                              color=disnake.Color.dark_theme())
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(
            text=f"Ведущий данного мероприятия {ctx.user.name}",
            icon_url=f"{avatar_url}"
        )
        view = View()
        view.add_item(ButtonConfirm(self))
        view.add_item(ButtonCancel(self))
        view_second = View()
        view_second.add_item(ButtonAccept(self))
        view_second.add_item(ButtonRerrol(self))
        await ctx.send(embed=embed, view=view, delete_after=time_in_seconds)
        await asyncio.sleep(time_in_seconds)
        selected_winner = random.choice(give_away_pool)
        selected_winner_user = await self.bot.fetch_user(selected_winner)

        if len(give_away_pool_user) < 1:
            embed_winner = disnake.Embed(title="Победитель Розыгрыша",
                                         description=f"Пользователь <@{selected_winner}> выиграл в розыгрыше\nОн получает **{prize}**\n",
                                         color=disnake.Color.dark_theme())
            embed_winner.set_thumbnail(url=selected_winner_user.display_avatar.url)
            embed_winner.set_footer(text="Нажмите ниже для реролла или выдачи награды")
            await ctx.send(embed=embed_winner, view=view_second)
        else:
            selected_winner = random.choice(give_away_pool_user)
            selected_winner_user = await self.bot.fetch_user(selected_winner)
            embed_winner = disnake.Embed(title="Победитель Розыгрыша",
                                         description=f"Пользователь <@{selected_winner}> выиграл в розыгрыше\nОн получает **{prize}**\n",
                                         color=disnake.Color.dark_theme())
            embed_winner.set_thumbnail(url=selected_winner_user.display_avatar.url)
            embed_winner.set_footer(text="Нажмите ниже для реролла или выдачи награды")
            await ctx.send(embed=embed_winner, view=view_second)

    @commands.command()
    @commands.has_any_role(1022510823404478556, 1035268469387706498)
    async def choose_winner(self, ctx, user: disnake.User):
        give_away_pool_user.append(user.id)
        await ctx.author.send(f"Выбран в качестве победителя <@{user.id}>")


def setup(bot):
    bot.add_cog(GiveAway(bot))

import { Link } from "react-router-dom";
import BrandMark from "../components/BrandMark";

export default function LegalPage() {
  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10 text-slate-800 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl rounded-[28px] border border-slate-200 bg-white p-6 shadow-[0_20px_60px_rgba(15,23,42,0.08)] sm:p-8 lg:p-12">
        <div className="mb-8 flex items-center gap-4">
          <BrandMark className="h-14 w-14" compact />
          <div>
            <div className="brand-word text-3xl font-black tracking-[-0.08em] text-slate-900">ProspectAI</div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Leadership intelligent de la prospection B2B</p>
          </div>
        </div>

        <h1 className="text-3xl font-black tracking-tight text-slate-900">Conditions d’utilisation</h1>
        <p className="mt-4 text-sm leading-7 text-slate-600">
          En accédant et en utilisant la plateforme ProspectAI, vous acceptez les présentes Conditions d’Utilisation.
          ProspectAI est une solution de gestion de prospection commerciale, de suivi de prospects et d’analyse assistée
          par intelligence artificielle destinée aux équipes commerciales et aux gestionnaires de pipeline.
        </p>

        <div className="mt-8 space-y-7 text-sm leading-7 text-slate-700">
          <section>
            <h2 className="text-lg font-bold text-slate-900">1. Objet du service</h2>
            <p>
              ProspectAI permet de gérer les prospects, suivre les interactions, organiser les activités commerciales et
              exploiter des outils d’analyse afin d’améliorer la qualification et le suivi des opportunités commerciales.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">2. Utilisation autorisée</h2>
            <p>
              L’utilisateur s’engage à utiliser la plateforme conformément à la législation en vigueur et à ne pas utiliser
              ProspectAI à des fins illégales, frauduleuses, trompeuses ou nuisibles. Il ne doit pas tenter d’accéder au
              service par des moyens non autorisés, contourner les protections techniques ou exploiter la plateforme d’une
              manière susceptible de nuire à son bon fonctionnement.
            </p>
            <p className="mt-2">
              L’utilisateur est responsable des informations, données, contacts et contenus qu’il renseigne dans la
              plateforme. Il doit s’assurer qu’il dispose des droits nécessaires pour exploiter ces données dans le cadre
              de l’utilisation du service.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">3. Responsabilité</h2>
            <p>
              ProspectAI est fournie en l’état, sans garantie expresse ou implicite concernant son bon fonctionnement, sa
              disponibilité ou son exhaustivité. Nous ne pouvons être tenus responsables des pertes, dommages,
              interruptions, erreurs de traitement ou conséquences liées à une utilisation inappropriée de la plateforme.
            </p>
            <p className="mt-2">
              Nous nous réservons le droit de suspendre, limiter ou interrompre l’accès à ProspectAI en cas de violation des
              présentes conditions, d’utilisation abusive ou de risque pour la sécurité, la qualité du service ou les droits
              des tiers.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">4. Données et sécurité</h2>
            <p>
              Nous mettons en œuvre des mesures de sécurité raisonnables pour protéger les données traitées dans le cadre du
              service. Toutefois, aucune solution numérique ne peut être garantie à 100 % exempte de risque. L’utilisateur
              doit prendre les mesures appropriées pour sécuriser ses accès et ses informations sensibles.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">5. Modifications</h2>
            <p>
              ProspectAI se réserve le droit de modifier les présentes Conditions d’Utilisation à tout moment. Les
              modifications prennent effet dès leur publication sur la plateforme. L’utilisation continue du service après
              publication vaut acceptation des nouvelles conditions.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">6. Propriété intellectuelle</h2>
            <p>
              Tous les éléments de la plateforme, y compris les textes, graphismes, logos, interfaces, contenus,
              fonctionnalités et structures, sont la propriété de ProspectAI ou de ses partenaires autorisés. Toute
              reproduction, diffusion ou exploitation non autorisée est interdite.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-bold text-slate-900">7. Loi applicable</h2>
            <p>
              Les présentes conditions sont régies par la législation en vigueur dans le pays où le service est exploité. En
              cas de litige, les parties tenteront de résoudre leur différend de manière amiable avant toute procédure
              judiciaire.
            </p>
          </section>
        </div>

        <p className="mt-8 text-sm text-slate-600">
          En utilisant ProspectAI, vous reconnaissez avoir lu, compris et accepté les présentes Conditions d’Utilisation.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Link to="/login" className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700">
            Retour à la connexion
          </Link>
          <Link to="/register" className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100">
            Créer un compte
          </Link>
        </div>
      </div>
    </div>
  );
}
